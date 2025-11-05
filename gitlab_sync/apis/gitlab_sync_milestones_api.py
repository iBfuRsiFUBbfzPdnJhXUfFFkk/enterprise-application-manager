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
    GitLabSyncJobTracker,
    GitLabSyncMilestone,
    GitLabSyncProject,
)
from gitlab_sync.utilities import (
    SyncResult,
    check_job_cancelled,
    handle_gitlab_api_errors,
    run_sync_in_background,
)


def _sync_milestones_background(
    request: HttpRequest, job_tracker: GitLabSyncJobTracker
) -> None:
    """Background function to sync milestones with progress tracking."""
    sync_result = SyncResult(
        entity_type="GitLabSyncMilestone", job_tracker_id=job_tracker.id
    )
    sync_result.add_log("Starting milestones sync...")

    git_lab_client: Gitlab | None = get_git_lab_client()
    if git_lab_client is None:
        sync_result.add_log("❌ Failed to get GitLab client")
        sync_result.add_failure("Failed to get GitLab client")
        sync_result.finish()
        print(f"[GitLabSync] {sync_result}")
        return

    # Sync project milestones
    projects: QuerySet[GitLabSyncProject] = cast_query_set(
        typ=GitLabSyncProject,
        val=GitLabSyncProject.objects.all(),
    )

    project_count = projects.count()
    sync_result.add_log(f"Syncing milestones from {project_count} projects...")

    for proj_idx, project in enumerate(projects, 1):
        if check_job_cancelled(sync_result.job_tracker_id):
            sync_result.add_log("⚠️ Job cancelled by user, stopping sync...")
            sync_result.finish()
            print(f"[GitLabSync] {sync_result}")
            return

        sync_result.update_progress(
            proj_idx - 1,
            project_count + 1,
            f"📥 Fetching milestones from project {project.path_with_namespace} ({proj_idx}/{project_count})...",
        )

        milestones, error = handle_gitlab_api_errors(
            func=lambda: [
                m.asdict()
                for m in git_lab_client.projects.get(id=project.id, lazy=True)
                .milestones.list(get_all=True)
            ],
            entity_name=f"Milestones for project {project.path_with_namespace}",
            max_retries=3,
        )

        if error:
            error_str = str(error).lower()
            if "403" in error_str or "forbidden" in error_str:
                sync_result.add_log(
                    f"⚠️ Access denied for milestones in {project.path_with_namespace} - skipping"
                )
                continue
            sync_result.add_log(
                f"❌ Error fetching milestones for {project.path_with_namespace}: {error}"
            )
            sync_result.add_failure(error)
            continue

        if not milestones:
            continue

        sync_result.add_log(
            f"✓ Fetched {len(milestones)} milestones from {project.path_with_namespace}"
        )

        for milestone_dict in milestones:
            if check_job_cancelled(sync_result.job_tracker_id):
                sync_result.add_log("⚠️ Job cancelled by user, stopping sync...")
                sync_result.finish()
                print(f"[GitLabSync] {sync_result}")
                return

            gitlab_id: int | None = milestone_dict.get("id")
            if gitlab_id is None:
                sync_result.add_skip()
                continue

            try:
                milestone, created = GitLabSyncMilestone.objects.get_or_create(
                    gitlab_id=gitlab_id, defaults={"project": project}
                )

                milestone.project = project
                milestone.title = milestone_dict.get("title")
                milestone.description = milestone_dict.get("description")
                milestone.state = milestone_dict.get("state")
                milestone.due_date = milestone_dict.get("due_date")
                milestone.start_date = milestone_dict.get("start_date")
                milestone.web_url = milestone_dict.get("web_url")
                milestone.created_at = convert_and_enforce_utc_timezone(
                    datetime_string=milestone_dict.get("created_at")
                )
                milestone.updated_at = convert_and_enforce_utc_timezone(
                    datetime_string=milestone_dict.get("updated_at")
                )

                milestone.save()
                sync_result.add_success()

            except Exception as error:
                import traceback

                error_trace = traceback.format_exc()
                error_msg = f"Failed to save milestone {gitlab_id}: {str(error)}"
                sync_result.add_failure(error_msg)
                sync_result.add_log(f"❌ {error_msg}")
                print(f"[GitLabSync] {error_msg}\n{error_trace}")
                continue

    # Sync group milestones
    groups: QuerySet[GitLabSyncGroup] = cast_query_set(
        typ=GitLabSyncGroup,
        val=GitLabSyncGroup.objects.all(),
    )

    group_count = groups.count()
    sync_result.add_log(f"Syncing milestones from {group_count} groups...")

    for grp_idx, group in enumerate(groups, 1):
        if check_job_cancelled(sync_result.job_tracker_id):
            sync_result.add_log("⚠️ Job cancelled by user, stopping sync...")
            sync_result.finish()
            print(f"[GitLabSync] {sync_result}")
            return

        sync_result.update_progress(
            project_count + grp_idx - 1,
            project_count + group_count,
            f"📥 Fetching milestones from group {group.path} ({grp_idx}/{group_count})...",
        )

        milestones, error = handle_gitlab_api_errors(
            func=lambda: [
                m.asdict()
                for m in git_lab_client.groups.get(id=group.id, lazy=True)
                .milestones.list(get_all=True)
            ],
            entity_name=f"Milestones for group {group.path}",
            max_retries=3,
        )

        if error:
            error_str = str(error).lower()
            if "403" in error_str or "forbidden" in error_str:
                sync_result.add_log(
                    f"⚠️ Access denied for milestones in {group.path} - skipping"
                )
                continue
            sync_result.add_log(
                f"❌ Error fetching milestones for {group.path}: {error}"
            )
            sync_result.add_failure(error)
            continue

        if not milestones:
            continue

        sync_result.add_log(f"✓ Fetched {len(milestones)} milestones from {group.path}")

        for milestone_dict in milestones:
            if check_job_cancelled(sync_result.job_tracker_id):
                sync_result.add_log("⚠️ Job cancelled by user, stopping sync...")
                sync_result.finish()
                print(f"[GitLabSync] {sync_result}")
                return

            gitlab_id: int | None = milestone_dict.get("id")
            if gitlab_id is None:
                sync_result.add_skip()
                continue

            try:
                milestone, created = GitLabSyncMilestone.objects.get_or_create(
                    gitlab_id=gitlab_id, defaults={"group": group}
                )

                milestone.group = group
                milestone.title = milestone_dict.get("title")
                milestone.description = milestone_dict.get("description")
                milestone.state = milestone_dict.get("state")
                milestone.due_date = milestone_dict.get("due_date")
                milestone.start_date = milestone_dict.get("start_date")
                milestone.web_url = milestone_dict.get("web_url")
                milestone.created_at = convert_and_enforce_utc_timezone(
                    datetime_string=milestone_dict.get("created_at")
                )
                milestone.updated_at = convert_and_enforce_utc_timezone(
                    datetime_string=milestone_dict.get("updated_at")
                )

                milestone.save()
                sync_result.add_success()

            except Exception as error:
                import traceback

                error_trace = traceback.format_exc()
                error_msg = f"Failed to save milestone {gitlab_id}: {str(error)}"
                sync_result.add_failure(error_msg)
                sync_result.add_log(f"❌ {error_msg}")
                print(f"[GitLabSync] {error_msg}\n{error_trace}")
                continue

    sync_result.update_progress(project_count + group_count, project_count + group_count, None)
    sync_result.add_log(
        f"✓ Sync complete: {sync_result.synced_count} synced, {sync_result.skipped_count} skipped, {sync_result.failed_count} failed"
    )
    sync_result.finish()
    print(f"[GitLabSync] {sync_result}")


def gitlab_sync_milestones_api(
    request: HttpRequest,
) -> JsonResponse | HttpResponse:
    """
    Sync milestones from GitLab EE 17.11.6 with background job tracking.

    New functionality for tracking project and group milestones.

    Returns immediately with job_id for progress tracking.
    """
    job_tracker = run_sync_in_background(
        "milestones", _sync_milestones_background, request
    )

    return JsonResponse(
        data={"success": True, "job_id": job_tracker.id, "job_type": "milestones"}
    )
