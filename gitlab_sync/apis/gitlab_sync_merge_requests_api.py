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
    GitLabSyncJobTracker,
    GitLabSyncMergeRequest,
    GitLabSyncPipeline,
    GitLabSyncProject,
    GitLabSyncUser,
)
from gitlab_sync.utilities import (
    SyncResult,
    check_job_cancelled,
    handle_gitlab_api_errors,
    run_sync_in_background,
)


def _sync_merge_requests_background(
    request: HttpRequest, job_tracker: GitLabSyncJobTracker
) -> None:
    """Background function to sync merge requests with progress tracking."""
    sync_result = SyncResult(
        entity_type="GitLabSyncMergeRequest", job_tracker_id=job_tracker.id
    )
    sync_result.add_log("Starting merge requests sync...")

    git_lab_client: Gitlab | None = get_git_lab_client()
    if git_lab_client is None:
        sync_result.add_log("❌ Failed to get GitLab client")
        sync_result.add_failure("Failed to get GitLab client")
        sync_result.finish()
        print(f"[GitLabSync] {sync_result}")
        return

    config = ThisServerConfiguration.current()
    max_merge_requests = config.coerced_gitlab_sync_max_merge_requests_per_project

    projects: QuerySet[GitLabSyncProject] = cast_query_set(
        typ=GitLabSyncProject,
        val=GitLabSyncProject.objects.all(),
    )

    project_count = projects.count()
    sync_result.add_log(
        f"Syncing merge requests from {project_count} projects (max {max_merge_requests} per project)..."
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
            f"📥 About to fetch merge requests from project {project.path_with_namespace} (project {proj_idx}/{project_count})...",
        )

        merge_requests, error = handle_gitlab_api_errors(
            func=lambda: [
                mr.asdict()
                for mr in git_lab_client.projects.get(id=project.id, lazy=True)
                .mergerequests.list(per_page=100, page=1, max_pages=max(1, max_merge_requests // 100))
            ],
            entity_name=f"Merge requests for project {project.path_with_namespace}",
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
                    f"⚠️ Access denied (403) for merge requests in {project.path_with_namespace} - skipping"
                )
                continue

            # For other errors, add as failure
            sync_result.add_log(
                f"❌ Error fetching merge requests for {project.path_with_namespace}: {error}"
            )
            sync_result.add_failure(error)
            continue

        if not merge_requests:
            sync_result.add_log(f"⊘ No merge requests found in project {project.path_with_namespace}")
            continue

        sync_result.add_log(f"✓ Fetched {len(merge_requests)} merge requests from {project.path_with_namespace}, about to process...")

        # Process each merge request immediately
        for mr_dict in merge_requests:
            # Check if job was cancelled
            if check_job_cancelled(sync_result.job_tracker_id):
                sync_result.add_log("⚠️ Job cancelled by user, stopping sync...")
                sync_result.finish()
                print(f"[GitLabSync] {sync_result}")
                return

            mr_id: int | None = mr_dict.get("id")

            if mr_id is None:
                sync_result.add_skip()
                continue

            try:
                sync_result.add_log(f"💾 About to get_or_create merge request {mr_id} in database...")
                merge_request, created = GitLabSyncMergeRequest.objects.get_or_create(
                    id=mr_id
                )
                sync_result.add_log(f"✓ Database get_or_create succeeded for merge request {mr_id} (created={created})")

                # Check if we need to update (compare updated_at from GitLab with our stored updated_at)
                mr_updated_at = convert_and_enforce_utc_timezone(
                    datetime_string=mr_dict.get("updated_at")
                )

                needs_update = created or (
                    merge_request.updated_at is None
                    or (
                        mr_updated_at
                        and mr_updated_at > merge_request.updated_at
                    )
                )

                if not needs_update:
                    sync_result.add_skip()
                    sync_result.add_log(f"⊘ Skipped unchanged merge request #{mr_id}")
                    continue

                # Update merge request fields
                merge_request.project = GitLabSyncProject.objects.filter(
                    id=project.id
                ).first()

                # Handle author
                author_dict = mr_dict.get("author")
                if author_dict:
                    user = GitLabSyncUser.objects.filter(id=author_dict.get("id")).first()
                    if user:
                        merge_request.author = user

                # Handle closed_by
                closed_by_dict = mr_dict.get("closed_by")
                if closed_by_dict:
                    user = GitLabSyncUser.objects.filter(id=closed_by_dict.get("id")).first()
                    if user:
                        merge_request.closed_by = user

                # Handle merged_by
                merged_by_dict = mr_dict.get("merged_by")
                if merged_by_dict:
                    user = GitLabSyncUser.objects.filter(id=merged_by_dict.get("id")).first()
                    if user:
                        merge_request.merged_by = user

                # Handle head_pipeline
                head_pipeline_dict = mr_dict.get("head_pipeline")
                if head_pipeline_dict:
                    pipeline = GitLabSyncPipeline.objects.filter(id=head_pipeline_dict.get("id")).first()
                    if pipeline:
                        merge_request.head_pipeline = pipeline

                merge_request.iid = mr_dict.get("iid")
                merge_request.title = mr_dict.get("title")
                merge_request.description = mr_dict.get("description")
                merge_request.state = mr_dict.get("state")
                merge_request.web_url = mr_dict.get("web_url")
                merge_request.references_short = mr_dict.get("references", {}).get("short")
                merge_request.references_relative = mr_dict.get("references", {}).get("relative")
                merge_request.references_full = mr_dict.get("references", {}).get("full")
                merge_request.has_tasks = mr_dict.get("has_tasks")
                merge_request.task_status = mr_dict.get("task_status")
                merge_request.task_completion_status_count = mr_dict.get("task_completion_status", {}).get("count")
                merge_request.task_completion_status_completed_count = mr_dict.get("task_completion_status", {}).get("completed_count")
                merge_request.time_stats_time_estimate = mr_dict.get("time_stats", {}).get("time_estimate")
                merge_request.time_stats_total_time_spent = mr_dict.get("time_stats", {}).get("total_time_spent")
                merge_request.time_stats_human_time_estimate = mr_dict.get("time_stats", {}).get("human_time_estimate")
                merge_request.time_stats_human_total_time_spent = mr_dict.get("time_stats", {}).get("human_total_time_spent")
                merge_request.blocking_discussions_resolved = mr_dict.get("blocking_discussions_resolved")
                merge_request.draft = mr_dict.get("draft")
                merge_request.has_conflicts = mr_dict.get("has_conflicts")
                merge_request.sha = mr_dict.get("sha")
                merge_request.source_branch = mr_dict.get("source_branch")
                merge_request.target_branch = mr_dict.get("target_branch")
                merge_request.squash = mr_dict.get("squash")
                merge_request.squash_commit_sha = mr_dict.get("squash_commit_sha")
                merge_request.merge_status = mr_dict.get("merge_status")
                merge_request.user_notes_count = mr_dict.get("user_notes_count")
                merge_request.upvotes = mr_dict.get("upvotes")
                merge_request.downvotes = mr_dict.get("downvotes")

                # Handle diff_refs
                diff_refs = mr_dict.get("diff_refs", {})
                if diff_refs:
                    merge_request.diff_refs_base_sha = diff_refs.get("base_sha")
                    merge_request.diff_refs_head_sha = diff_refs.get("head_sha")
                    merge_request.diff_refs_start_sha = diff_refs.get("start_sha")

                merge_request.created_at = convert_and_enforce_utc_timezone(
                    datetime_string=mr_dict.get("created_at")
                )
                merge_request.updated_at = mr_updated_at
                merge_request.closed_at = convert_and_enforce_utc_timezone(
                    datetime_string=mr_dict.get("closed_at")
                )
                merge_request.merged_at = convert_and_enforce_utc_timezone(
                    datetime_string=mr_dict.get("merged_at")
                )
                merge_request.prepared_at = convert_and_enforce_utc_timezone(
                    datetime_string=mr_dict.get("prepared_at")
                )

                sync_result.add_log(f"💾 About to save merge request {mr_id} to database...")
                merge_request.save()
                sync_result.add_log(f"✓ Database save succeeded for merge request {mr_id}")

                # Handle many-to-many assignees
                assignees_data = mr_dict.get("assignees", [])
                if assignees_data:
                    assignee_ids = [a.get("id") for a in assignees_data if a.get("id")]
                    assignees = GitLabSyncUser.objects.filter(id__in=assignee_ids)
                    merge_request.assignees.set(assignees)

                # Handle many-to-many reviewers
                reviewers_data = mr_dict.get("reviewers", [])
                if reviewers_data:
                    reviewer_ids = [r.get("id") for r in reviewers_data if r.get("id")]
                    reviewers = GitLabSyncUser.objects.filter(id__in=reviewer_ids)
                    merge_request.reviewers.set(reviewers)

                sync_result.add_success()

            except Exception as error:
                import traceback
                error_trace = traceback.format_exc()
                error_msg = f"Failed to save merge request {mr_id}: {str(error)}"
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


def gitlab_sync_merge_requests_api(
    request: HttpRequest,
) -> JsonResponse | HttpResponse:
    """
    Sync merge requests from GitLab EE 17.11.6 with background job tracking.

    New functionality not present in the original git_lab app.
    Tracks merge requests for code review and deployment.

    Returns immediately with job_id for progress tracking.
    """
    job_tracker = run_sync_in_background("merge-requests", _sync_merge_requests_background, request)

    return JsonResponse(
        data={"success": True, "job_id": job_tracker.id, "job_type": "merge-requests"}
    )
