from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils import timezone
from gitlab import Gitlab

from core.utilities.cast_query_set import cast_query_set
from core.utilities.convert_and_enforce_utc_timezone import (
    convert_and_enforce_utc_timezone,
)
from core.utilities.git_lab.get_git_lab_client import get_git_lab_client
from gitlab_sync.models import (
    GitLabSyncJobTracker,
    GitLabSyncProject,
    GitLabSyncUser,
    GitLabSyncVulnerability,
)
from gitlab_sync.utilities import (
    SyncResult,
    check_job_cancelled,
    handle_gitlab_api_errors,
    run_sync_in_background,
)


def _sync_vulnerabilities_background(
    request: HttpRequest, job_tracker: GitLabSyncJobTracker
) -> None:
    """Background function to sync vulnerabilities with progress tracking."""
    sync_result = SyncResult(
        entity_type="GitLabSyncVulnerability", job_tracker_id=job_tracker.id
    )
    sync_result.add_log("Starting vulnerabilities sync (GitLab EE security feature)...")

    git_lab_client: Gitlab | None = get_git_lab_client()
    if git_lab_client is None:
        sync_result.add_log("❌ Failed to get GitLab client")
        sync_result.add_failure("Failed to get GitLab client")
        sync_result.finish()
        print(f"[GitLabSync] {sync_result}")
        return

    projects: QuerySet[GitLabSyncProject] = cast_query_set(
        typ=GitLabSyncProject,
        val=GitLabSyncProject.objects.all(),
    )

    project_count = projects.count()
    sync_result.add_log(
        f"Syncing vulnerabilities from {project_count} projects incrementally..."
    )

    for proj_idx, project in enumerate(projects, 1):
        # Check if job was cancelled
        if check_job_cancelled(sync_result.job_tracker_id):
            sync_result.add_log("⚠️ Job cancelled by user, stopping sync...")
            sync_result.finish()
            print(f"[GitLabSync] {sync_result}")
            return

        # Update progress at project level
        sync_result.update_progress(
            proj_idx - 1,
            project_count,
            f"📥 About to fetch vulnerabilities from project {project.path_with_namespace} (project {proj_idx}/{project_count})...",
        )

        # Try to fetch vulnerabilities using the project vulnerability_findings endpoint
        # This is the correct endpoint for GitLab Ultimate
        vulnerabilities, error = handle_gitlab_api_errors(
            func=lambda: [
                v.asdict()
                for v in git_lab_client.projects.get(id=project.id, lazy=False)
                .vulnerability_findings.list(get_all=True)
            ],
            entity_name=f"Vulnerabilities for project {project.path_with_namespace}",
            max_retries=3,
        )

        if error:
            # Check if this is a 403 Forbidden error or feature not available - if so, just log and continue
            error_str = str(error).lower()
            if (
                "403" in error_str
                or "forbidden" in error_str
                or "access denied" in error_str
                or "permission denied" in error_str
                or "404" in error_str
                or "not found" in error_str
                or "ultimate" in error_str
            ):
                sync_result.add_log(
                    f"⚠️ Vulnerabilities not available for project {project.path_with_namespace} (may require GitLab EE Ultimate) - skipping"
                )
                continue

            # For other errors, add as failure
            sync_result.add_log(
                f"❌ Error fetching vulnerabilities for {project.path_with_namespace}: {error}"
            )
            sync_result.add_failure(error)
            continue

        if not vulnerabilities:
            sync_result.add_log(f"⊘ No vulnerabilities found in project {project.path_with_namespace}")
            continue

        sync_result.add_log(f"✓ Fetched {len(vulnerabilities)} vulnerabilities from {project.path_with_namespace}, about to process...")

        # Process each vulnerability immediately
        for vuln_dict in vulnerabilities:
            # Check if job was cancelled
            if check_job_cancelled(sync_result.job_tracker_id):
                sync_result.add_log("⚠️ Job cancelled by user, stopping sync...")
                sync_result.finish()
                print(f"[GitLabSync] {sync_result}")
                return

            vuln_id: int | None = vuln_dict.get("id")

            if vuln_id is None:
                sync_result.add_skip()
                continue

            try:
                sync_result.add_log(f"💾 About to get_or_create vulnerability {vuln_id} in database...")
                vulnerability, created = GitLabSyncVulnerability.objects.get_or_create(
                    id=vuln_id
                )
                sync_result.add_log(f"✓ Database get_or_create succeeded for vulnerability {vuln_id} (created={created})")

                # Check if we need to update (compare updated_at from GitLab with our last_synced_at)
                vuln_updated_at = convert_and_enforce_utc_timezone(
                    datetime_string=vuln_dict.get("updated_at")
                )

                needs_update = created or (
                    vulnerability.last_synced_at is None
                    or (
                        vuln_updated_at
                        and vuln_updated_at > vulnerability.last_synced_at
                    )
                )

                if not needs_update:
                    sync_result.add_skip()
                    sync_result.add_log(f"⊘ Skipped unchanged vulnerability #{vuln_id}")
                    continue

                # Update vulnerability fields
                vulnerability.project = GitLabSyncProject.objects.filter(
                    id=project.id
                ).first()

                # Handle author
                author_dict = vuln_dict.get("author")
                if author_dict:
                    user = GitLabSyncUser.objects.filter(id=author_dict.get("id")).first()
                    if user:
                        vulnerability.author = user

                # Handle resolved_by
                resolved_by_dict = vuln_dict.get("resolved_by")
                if resolved_by_dict:
                    user = GitLabSyncUser.objects.filter(id=resolved_by_dict.get("id")).first()
                    if user:
                        vulnerability.resolved_by = user

                # Handle dismissed_by
                dismissed_by_dict = vuln_dict.get("dismissed_by")
                if dismissed_by_dict:
                    user = GitLabSyncUser.objects.filter(id=dismissed_by_dict.get("id")).first()
                    if user:
                        vulnerability.dismissed_by = user

                vulnerability.title = vuln_dict.get("title")
                vulnerability.description = vuln_dict.get("description")
                vulnerability.state = vuln_dict.get("state")
                vulnerability.severity = vuln_dict.get("severity")
                vulnerability.confidence = vuln_dict.get("confidence")
                vulnerability.report_type = vuln_dict.get("report_type")
                vulnerability.finding_id = vuln_dict.get("finding", {}).get("id") if vuln_dict.get("finding") else None

                # Handle scanner information
                scanner = vuln_dict.get("scanner", {})
                if scanner:
                    vulnerability.scanner_name = scanner.get("name")
                    vulnerability.scanner_vendor = scanner.get("vendor")

                # Handle identifiers (store as JSON string)
                identifiers = vuln_dict.get("identifiers", [])
                if identifiers:
                    import json
                    vulnerability.identifiers = json.dumps(identifiers)

                # Handle links (store as JSON string)
                links = vuln_dict.get("links", [])
                if links:
                    import json
                    vulnerability.links = json.dumps(links)

                # Handle location information
                location = vuln_dict.get("location", {})
                if location:
                    vulnerability.location_file = location.get("file")
                    vulnerability.location_start_line = location.get("start_line")
                    vulnerability.location_end_line = location.get("end_line")
                    vulnerability.location_class = location.get("class")
                    vulnerability.location_method = location.get("method")
                    vulnerability.location_dependency = location.get("dependency", {}).get("package", {}).get("name") if location.get("dependency") else None
                    vulnerability.location_image = location.get("image")
                    vulnerability.location_operating_system = location.get("operating_system")

                vulnerability.created_at = convert_and_enforce_utc_timezone(
                    datetime_string=vuln_dict.get("created_at")
                )
                vulnerability.updated_at = vuln_updated_at
                vulnerability.detected_at = convert_and_enforce_utc_timezone(
                    datetime_string=vuln_dict.get("detected_at")
                )
                vulnerability.resolved_at = convert_and_enforce_utc_timezone(
                    datetime_string=vuln_dict.get("resolved_at")
                )
                vulnerability.dismissed_at = convert_and_enforce_utc_timezone(
                    datetime_string=vuln_dict.get("dismissed_at")
                )
                vulnerability.last_synced_at = timezone.now()

                sync_result.add_log(f"💾 About to save vulnerability {vuln_id} to database...")
                vulnerability.save()
                sync_result.add_log(f"✓ Database save succeeded for vulnerability {vuln_id}")
                sync_result.add_success()

            except Exception as error:
                import traceback
                error_trace = traceback.format_exc()
                error_msg = f"Failed to save vulnerability {vuln_id}: {str(error)}"
                sync_result.add_failure(error_msg)
                sync_result.add_log(f"❌ {error_msg}")
                print(f"[GitLabSync] {error_msg}")
                print(f"[GitLabSync] Stack trace:\n{error_trace}")
                continue

    # Final progress update
    sync_result.update_progress(project_count, project_count, None)

    sync_result.add_log(
        f"✓ Sync complete: {sync_result.synced_count} synced, "
        f"{sync_result.skipped_count} skipped, {sync_result.failed_count} failed"
    )
    sync_result.finish()
    print(f"[GitLabSync] {sync_result}")


def gitlab_sync_vulnerabilities_api(
    request: HttpRequest,
) -> JsonResponse | HttpResponse:
    """
    Sync vulnerabilities from GitLab EE 17.11.6 with background job tracking.

    New functionality not present in the original git_lab app.
    Tracks security vulnerabilities (GitLab EE Ultimate feature) from security scans.

    Returns immediately with job_id for progress tracking.
    """
    job_tracker = run_sync_in_background("vulnerabilities", _sync_vulnerabilities_background, request)

    return JsonResponse(
        data={"success": True, "job_id": job_tracker.id, "job_type": "vulnerabilities"}
    )
