from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, JsonResponse
from gitlab import Gitlab

from core.utilities.cast_query_set import cast_query_set
from core.utilities.convert_and_enforce_utc_timezone import (
    convert_and_enforce_utc_timezone,
)
from core.utilities.git_lab.get_git_lab_client import get_git_lab_client
from gitlab_sync.models import (
    GitLabSyncJobTracker,
    GitLabSyncProject,
    GitLabSyncRepository,
    GitLabSyncTag,
)
from gitlab_sync.utilities import (
    SyncResult,
    check_job_cancelled,
    handle_gitlab_api_errors,
    run_sync_in_background,
)


def _sync_tags_background(
    request: HttpRequest, job_tracker: GitLabSyncJobTracker
) -> None:
    """Background function to sync tags with progress tracking."""
    sync_result = SyncResult(
        entity_type="GitLabSyncTag", job_tracker_id=job_tracker.id
    )
    sync_result.add_log("Starting tags sync...")

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
        f"Syncing tags from {project_count} projects..."
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
            f"📥 About to fetch tags from project {project.path_with_namespace} (project {proj_idx}/{project_count})...",
        )

        tags, error = handle_gitlab_api_errors(
            func=lambda: [
                t.asdict()
                for t in git_lab_client.projects.get(id=project.id, lazy=True)
                .tags.list(get_all=True)
            ],
            entity_name=f"Tags for project {project.path_with_namespace}",
            max_retries=3,
        )

        if error:
            # Check if this is a 403 Forbidden error - if so, just log and continue without failing
            error_str = str(error).lower()
            if (
                "403" in error_str
                or "forbidden" in error_str
                or "access denied" in error_str
                or "permission denied" in error_str
            ):
                sync_result.add_log(
                    f"⚠️ Access denied (403) for tags in {project.path_with_namespace} - skipping"
                )
                continue

            # For other errors, add as failure
            sync_result.add_log(
                f"❌ Error fetching tags for {project.path_with_namespace}: {error}"
            )
            sync_result.add_failure(error)
            continue

        if not tags:
            sync_result.add_log(f"⊘ No tags found in project {project.path_with_namespace}")
            continue

        sync_result.add_log(f"✓ Fetched {len(tags)} tags from {project.path_with_namespace}, about to process...")

        # Get or create repository for this project
        repository = None
        try:
            repository, _ = GitLabSyncRepository.objects.get_or_create(
                project=project,
                defaults={"name": f"{project.name} Repository"}
            )
        except Exception as repo_error:
            sync_result.add_log(f"⚠️ Could not create repository for project {project.id}: {repo_error}")

        # Process each tag immediately
        for tag_dict in tags:
            # Check if job was cancelled
            if check_job_cancelled(sync_result.job_tracker_id):
                sync_result.add_log("⚠️ Job cancelled by user, stopping sync...")
                sync_result.finish()
                print(f"[GitLabSync] {sync_result}")
                return

            tag_name: str | None = tag_dict.get("name")

            if tag_name is None:
                sync_result.add_skip()
                continue

            try:
                sync_result.add_log(f"💾 About to get_or_create tag {tag_name} in database...")
                tag, created = GitLabSyncTag.objects.get_or_create(
                    project=project,
                    name=tag_name,
                    defaults={}
                )
                sync_result.add_log(f"✓ Database get_or_create succeeded for tag {tag_name} (created={created})")

                # Update tag fields
                tag.project = project
                if repository:
                    tag.repository = repository

                tag.name = tag_name
                tag.message = tag_dict.get("message")
                tag.target = tag_dict.get("target")
                tag.protected = tag_dict.get("protected")

                # Handle release info
                release = tag_dict.get("release")
                if release:
                    tag.release_description = release.get("description")

                # Handle commit info
                commit = tag_dict.get("commit")
                if commit:
                    tag.commit_sha = commit.get("id")
                    tag.commit_short_id = commit.get("short_id")
                    tag.commit_title = commit.get("title")
                    tag.commit_message = commit.get("message")
                    tag.commit_created_at = convert_and_enforce_utc_timezone(
                        datetime_string=commit.get("created_at")
                    )

                sync_result.add_log(f"💾 About to save tag {tag_name} to database...")
                tag.save()
                sync_result.add_log(f"✓ Database save succeeded for tag {tag_name}")
                sync_result.add_success()

            except Exception as error:
                import traceback
                error_trace = traceback.format_exc()
                error_msg = f"Failed to save tag {tag_name if tag_name else 'unknown'}: {str(error)}"
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


def gitlab_sync_tags_api(
    request: HttpRequest,
) -> JsonResponse | HttpResponse:
    """
    Sync tags from GitLab EE 17.11.6 with background job tracking.

    New functionality not present in the original git_lab app.
    Tracks Git tags (version releases).

    Returns immediately with job_id for progress tracking.
    """
    job_tracker = run_sync_in_background("tags", _sync_tags_background, request)

    return JsonResponse(
        data={"success": True, "job_id": job_tracker.id, "job_type": "tags"}
    )
