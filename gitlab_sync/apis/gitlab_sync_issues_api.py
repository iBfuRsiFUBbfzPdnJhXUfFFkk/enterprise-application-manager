from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils import timezone
from gitlab import Gitlab

from core.models.this_server_configuration import ThisServerConfiguration
from core.utilities.cast_query_set import cast_query_set
from core.utilities.convert_and_enforce_utc_timezone import (
    convert_and_enforce_utc_timezone,
)
from core.utilities.git_lab.get_git_lab_client import get_git_lab_client
from gitlab_sync.models import (
    GitLabSyncEpic,
    GitLabSyncIssue,
    GitLabSyncJobTracker,
    GitLabSyncProject,
    GitLabSyncUser,
)
from gitlab_sync.utilities import (
    SyncResult,
    check_job_cancelled,
    handle_gitlab_api_errors,
    run_sync_in_background,
)


def _sync_issues_background(
    request: HttpRequest, job_tracker: GitLabSyncJobTracker
) -> None:
    """Background function to sync issues with progress tracking."""
    sync_result = SyncResult(
        entity_type="GitLabSyncIssue", job_tracker_id=job_tracker.id
    )
    sync_result.add_log("Starting issues sync...")

    git_lab_client: Gitlab | None = get_git_lab_client()
    if git_lab_client is None:
        sync_result.add_log("❌ Failed to get GitLab client")
        sync_result.add_failure("Failed to get GitLab client")
        sync_result.finish()
        print(f"[GitLabSync] {sync_result}")
        return

    config = ThisServerConfiguration.current()
    max_issues = config.coerced_gitlab_sync_max_issues_per_project

    projects: QuerySet[GitLabSyncProject] = cast_query_set(
        typ=GitLabSyncProject,
        val=GitLabSyncProject.objects.all(),
    )

    project_count = projects.count()
    sync_result.add_log(
        f"Syncing issues from {project_count} projects (max {max_issues} per project)..."
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
            f"📥 About to fetch issues from project {project.path_with_namespace} (project {proj_idx}/{project_count})...",
        )

        issues, error = handle_gitlab_api_errors(
            func=lambda: [
                i.asdict()
                for i in git_lab_client.projects.get(id=project.id, lazy=True)
                .issues.list(per_page=100, page=1, max_pages=max(1, max_issues // 100))
            ],
            entity_name=f"Issues for project {project.path_with_namespace}",
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
                    f"⚠️ Access denied (403) for issues in {project.path_with_namespace} - skipping"
                )
                continue

            # For other errors, add as failure
            sync_result.add_log(
                f"❌ Error fetching issues for {project.path_with_namespace}: {error}"
            )
            sync_result.add_failure(error)
            continue

        if not issues:
            sync_result.add_log(f"⊘ No issues found in project {project.path_with_namespace}")
            continue

        sync_result.add_log(f"✓ Fetched {len(issues)} issues from {project.path_with_namespace}, about to process...")

        # Process each issue immediately
        for issue_dict in issues:
            # Check if job was cancelled
            if check_job_cancelled(sync_result.job_tracker_id):
                sync_result.add_log("⚠️ Job cancelled by user, stopping sync...")
                sync_result.finish()
                print(f"[GitLabSync] {sync_result}")
                return

            issue_id: int | None = issue_dict.get("id")

            if issue_id is None:
                sync_result.add_skip()
                continue

            try:
                sync_result.add_log(f"💾 About to get_or_create issue {issue_id} in database...")
                issue, created = GitLabSyncIssue.objects.get_or_create(
                    id=issue_id
                )
                sync_result.add_log(f"✓ Database get_or_create succeeded for issue {issue_id} (created={created})")

                # Check if we need to update (compare updated_at from GitLab with our stored updated_at)
                issue_updated_at = convert_and_enforce_utc_timezone(
                    datetime_string=issue_dict.get("updated_at")
                )

                needs_update = created or (
                    issue.updated_at is None
                    or (
                        issue_updated_at
                        and issue_updated_at > issue.updated_at
                    )
                )

                if not needs_update:
                    sync_result.add_skip()
                    sync_result.add_log(f"⊘ Skipped unchanged issue #{issue_id}")
                    continue

                # Update issue fields
                issue.project = GitLabSyncProject.objects.filter(
                    id=project.id
                ).first()

                # Handle author
                author_dict = issue_dict.get("author")
                if author_dict:
                    user = GitLabSyncUser.objects.filter(id=author_dict.get("id")).first()
                    if user:
                        issue.author = user

                # Handle closed_by
                closed_by_dict = issue_dict.get("closed_by")
                if closed_by_dict:
                    user = GitLabSyncUser.objects.filter(id=closed_by_dict.get("id")).first()
                    if user:
                        issue.closed_by = user

                # Handle epic
                epic_dict = issue_dict.get("epic")
                if epic_dict:
                    epic = GitLabSyncEpic.objects.filter(id=epic_dict.get("id")).first()
                    if epic:
                        issue.epic = epic

                issue.iid = issue_dict.get("iid")
                issue.title = issue_dict.get("title")
                issue.description = issue_dict.get("description")
                issue.state = issue_dict.get("state")
                issue.web_url = issue_dict.get("web_url")
                issue.references_short = issue_dict.get("references", {}).get("short")
                issue.references_relative = issue_dict.get("references", {}).get("relative")
                issue.references_full = issue_dict.get("references", {}).get("full")
                issue.has_tasks = issue_dict.get("has_tasks")
                issue.task_status = issue_dict.get("task_status")
                issue.task_completion_status_count = issue_dict.get("task_completion_status", {}).get("count")
                issue.task_completion_status_completed_count = issue_dict.get("task_completion_status", {}).get("completed_count")
                issue.time_stats_time_estimate = issue_dict.get("time_stats", {}).get("time_estimate")
                issue.time_stats_total_time_spent = issue_dict.get("time_stats", {}).get("total_time_spent")
                issue.time_stats_human_time_estimate = issue_dict.get("time_stats", {}).get("human_time_estimate")
                issue.time_stats_human_total_time_spent = issue_dict.get("time_stats", {}).get("human_total_time_spent")
                issue.blocking_issues_count = issue_dict.get("blocking_issues_count")
                issue.issue_type = issue_dict.get("issue_type")
                issue.type = issue_dict.get("type")
                issue.user_notes_count = issue_dict.get("user_notes_count")
                issue.weight = issue_dict.get("weight")
                issue.severity = issue_dict.get("severity")
                issue.due_date = issue_dict.get("due_date")
                issue.confidential = issue_dict.get("confidential")

                issue.created_at = convert_and_enforce_utc_timezone(
                    datetime_string=issue_dict.get("created_at")
                )
                issue.updated_at = issue_updated_at
                issue.closed_at = convert_and_enforce_utc_timezone(
                    datetime_string=issue_dict.get("closed_at")
                )

                sync_result.add_log(f"💾 About to save issue {issue_id} to database...")
                issue.save()
                sync_result.add_log(f"✓ Database save succeeded for issue {issue_id}")

                # Handle many-to-many assignees
                assignees_data = issue_dict.get("assignees", [])
                if assignees_data:
                    assignee_ids = [a.get("id") for a in assignees_data if a.get("id")]
                    assignees = GitLabSyncUser.objects.filter(id__in=assignee_ids)
                    issue.assignees.set(assignees)

                sync_result.add_success()

            except Exception as error:
                import traceback
                error_trace = traceback.format_exc()
                error_msg = f"Failed to save issue {issue_id}: {str(error)}"
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


def gitlab_sync_issues_api(
    request: HttpRequest,
) -> JsonResponse | HttpResponse:
    """
    Sync issues from GitLab EE 17.11.6 with background job tracking.

    New functionality not present in the original git_lab app.
    Tracks issues for project management and tracking.

    Returns immediately with job_id for progress tracking.
    """
    job_tracker = run_sync_in_background("issues", _sync_issues_background, request)

    return JsonResponse(
        data={"success": True, "job_id": job_tracker.id, "job_type": "issues"}
    )
