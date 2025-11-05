from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, JsonResponse
from gitlab import Gitlab

from core.utilities.cast_query_set import cast_query_set
from core.utilities.convert_and_enforce_utc_timezone import (
    convert_and_enforce_utc_timezone,
)
from core.utilities.git_lab.get_git_lab_client import get_git_lab_client
from gitlab_sync.models import (
    GitLabSyncGroup,
    GitLabSyncIteration,
    GitLabSyncJobTracker,
)
from gitlab_sync.utilities import (
    SyncResult,
    check_job_cancelled,
    handle_gitlab_api_errors,
    run_sync_in_background,
)


def _sync_iterations_background(
    request: HttpRequest, job_tracker: GitLabSyncJobTracker
) -> None:
    """Background function to sync iterations with progress tracking."""
    sync_result = SyncResult(
        entity_type="GitLabSyncIteration", job_tracker_id=job_tracker.id
    )
    sync_result.add_log("Starting iterations sync...")

    git_lab_client: Gitlab | None = get_git_lab_client()
    if git_lab_client is None:
        sync_result.add_log("❌ Failed to get GitLab client")
        sync_result.add_failure("Failed to get GitLab client")
        sync_result.finish()
        print(f"[GitLabSync] {sync_result}")
        return

    groups: QuerySet[GitLabSyncGroup] = cast_query_set(
        typ=GitLabSyncGroup,
        val=GitLabSyncGroup.objects.all(),
    )

    group_count = groups.count()
    sync_result.add_log(f"Syncing iterations from {group_count} groups...")

    for grp_idx, group in enumerate(groups, 1):
        if check_job_cancelled(sync_result.job_tracker_id):
            sync_result.add_log("⚠️ Job cancelled by user, stopping sync...")
            sync_result.finish()
            print(f"[GitLabSync] {sync_result}")
            return

        sync_result.update_progress(
            grp_idx - 1,
            group_count,
            f"📥 Fetching iterations from group {group.path} ({grp_idx}/{group_count})...",
        )

        iterations, error = handle_gitlab_api_errors(
            func=lambda: [
                i.asdict()
                for i in git_lab_client.groups.get(id=group.id, lazy=True)
                .iterations.list(get_all=True)
            ],
            entity_name=f"Iterations for group {group.path}",
            max_retries=3,
        )

        if error:
            error_str = str(error).lower()
            if "403" in error_str or "forbidden" in error_str:
                sync_result.add_log(
                    f"⚠️ Access denied for iterations in {group.path} - skipping"
                )
                continue
            sync_result.add_log(f"❌ Error fetching iterations for {group.path}: {error}")
            sync_result.add_failure(error)
            continue

        if not iterations:
            continue

        sync_result.add_log(f"✓ Fetched {len(iterations)} iterations from {group.path}")

        for iteration_dict in iterations:
            if check_job_cancelled(sync_result.job_tracker_id):
                sync_result.add_log("⚠️ Job cancelled by user, stopping sync...")
                sync_result.finish()
                print(f"[GitLabSync] {sync_result}")
                return

            gitlab_id: int | None = iteration_dict.get("id")
            if gitlab_id is None:
                sync_result.add_skip()
                continue

            try:
                iteration, created = GitLabSyncIteration.objects.get_or_create(
                    gitlab_id=gitlab_id, defaults={"group": group}
                )

                iteration.group = group
                iteration.title = iteration_dict.get("title")
                iteration.description = iteration_dict.get("description")
                iteration.state = iteration_dict.get("state")
                iteration.due_date = iteration_dict.get("due_date")
                iteration.start_date = iteration_dict.get("start_date")
                iteration.sequence = iteration_dict.get("sequence")
                iteration.web_url = iteration_dict.get("web_url")
                iteration.created_at = convert_and_enforce_utc_timezone(
                    datetime_string=iteration_dict.get("created_at")
                )
                iteration.updated_at = convert_and_enforce_utc_timezone(
                    datetime_string=iteration_dict.get("updated_at")
                )

                iteration.save()
                sync_result.add_success()

            except Exception as error:
                import traceback

                error_trace = traceback.format_exc()
                error_msg = f"Failed to save iteration {gitlab_id}: {str(error)}"
                sync_result.add_failure(error_msg)
                sync_result.add_log(f"❌ {error_msg}")
                print(f"[GitLabSync] {error_msg}\n{error_trace}")
                continue

    sync_result.update_progress(group_count, group_count, None)
    sync_result.add_log(
        f"✓ Sync complete: {sync_result.synced_count} synced, {sync_result.skipped_count} skipped, {sync_result.failed_count} failed"
    )
    sync_result.finish()
    print(f"[GitLabSync] {sync_result}")


def gitlab_sync_iterations_api(
    request: HttpRequest,
) -> JsonResponse | HttpResponse:
    """
    Sync iterations from GitLab EE 17.11.6 with background job tracking.

    Iterations are group-level time-boxed periods for agile planning.

    Returns immediately with job_id for progress tracking.
    """
    job_tracker = run_sync_in_background(
        "iterations", _sync_iterations_background, request
    )

    return JsonResponse(
        data={"success": True, "job_id": job_tracker.id, "job_type": "iterations"}
    )
