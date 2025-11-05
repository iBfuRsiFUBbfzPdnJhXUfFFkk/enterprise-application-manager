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
    GitLabSyncEpic,
    GitLabSyncGroup,
    GitLabSyncJobTracker,
    GitLabSyncUser,
)
from gitlab_sync.utilities import (
    SyncResult,
    check_job_cancelled,
    handle_gitlab_api_errors,
    run_sync_in_background,
)


def _sync_epics_background(
    request: HttpRequest, job_tracker: GitLabSyncJobTracker
) -> None:
    """Background function to sync epics with progress tracking."""
    sync_result = SyncResult(
        entity_type="GitLabSyncEpic", job_tracker_id=job_tracker.id
    )
    sync_result.add_log("Starting epics sync (GitLab EE feature)...")

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
    sync_result.add_log(
        f"Syncing epics from {group_count} groups incrementally..."
    )

    for group_idx, group in enumerate(groups, 1):
        # Check if job was cancelled
        if check_job_cancelled(sync_result.job_tracker_id):
            sync_result.add_log("⚠️ Job cancelled by user, stopping sync...")
            sync_result.finish()
            print(f"[GitLabSync] {sync_result}")
            return

        # Update progress at group level
        sync_result.update_progress(
            group_idx - 1,
            group_count,
            f"📥 About to fetch epics from group {group.full_path} (group {group_idx}/{group_count})...",
        )

        epics, error = handle_gitlab_api_errors(
            func=lambda: [
                e.asdict()
                for e in git_lab_client.groups.get(id=group.id, lazy=True)
                .epics.list(get_all=True)
            ],
            entity_name=f"Epics for group {group.full_path}",
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
                or "premium" in error_str
                or "ultimate" in error_str
            ):
                sync_result.add_log(
                    f"⚠️ Epics not available for group {group.full_path} (may require GitLab EE Premium/Ultimate) - skipping"
                )
                continue

            # For other errors, add as failure
            sync_result.add_log(
                f"❌ Error fetching epics for {group.full_path}: {error}"
            )
            sync_result.add_failure(error)
            continue

        if not epics:
            sync_result.add_log(f"⊘ No epics found in group {group.full_path}")
            continue

        sync_result.add_log(f"✓ Fetched {len(epics)} epics from {group.full_path}, about to process...")

        # Process each epic immediately
        for epic_dict in epics:
            # Check if job was cancelled
            if check_job_cancelled(sync_result.job_tracker_id):
                sync_result.add_log("⚠️ Job cancelled by user, stopping sync...")
                sync_result.finish()
                print(f"[GitLabSync] {sync_result}")
                return

            epic_id: int | None = epic_dict.get("id")

            if epic_id is None:
                sync_result.add_skip()
                continue

            try:
                sync_result.add_log(f"💾 About to get_or_create epic {epic_id} in database...")
                epic, created = GitLabSyncEpic.objects.get_or_create(
                    id=epic_id
                )
                sync_result.add_log(f"✓ Database get_or_create succeeded for epic {epic_id} (created={created})")

                # Check if we need to update (compare updated_at from GitLab with our last_synced_at)
                epic_updated_at = convert_and_enforce_utc_timezone(
                    datetime_string=epic_dict.get("updated_at")
                )

                needs_update = created or (
                    epic.last_synced_at is None
                    or (
                        epic_updated_at
                        and epic_updated_at > epic.last_synced_at
                    )
                )

                if not needs_update:
                    sync_result.add_skip()
                    sync_result.add_log(f"⊘ Skipped unchanged epic #{epic_id}")
                    continue

                # Update epic fields
                epic.group = GitLabSyncGroup.objects.filter(
                    id=group.id
                ).first()

                # Handle author
                author_dict = epic_dict.get("author")
                if author_dict:
                    user = GitLabSyncUser.objects.filter(id=author_dict.get("id")).first()
                    if user:
                        epic.author = user

                # Handle parent epic
                parent_dict = epic_dict.get("parent")
                if parent_dict:
                    parent_epic = GitLabSyncEpic.objects.filter(id=parent_dict.get("id")).first()
                    if parent_epic:
                        epic.parent_epic = parent_epic

                epic.iid = epic_dict.get("iid")
                epic.title = epic_dict.get("title")
                epic.description = epic_dict.get("description")
                epic.state = epic_dict.get("state")
                epic.web_url = epic_dict.get("web_url")
                epic.upvotes = epic_dict.get("upvotes")
                epic.downvotes = epic_dict.get("downvotes")
                epic.user_notes_count = epic_dict.get("user_notes_count")
                epic.confidential = epic_dict.get("confidential")
                epic.color = epic_dict.get("color")
                epic.start_date_is_fixed = epic_dict.get("start_date_is_fixed")
                epic.due_date_is_fixed = epic_dict.get("due_date_is_fixed")

                epic.created_at = convert_and_enforce_utc_timezone(
                    datetime_string=epic_dict.get("created_at")
                )
                epic.updated_at = epic_updated_at
                epic.closed_at = convert_and_enforce_utc_timezone(
                    datetime_string=epic_dict.get("closed_at")
                )
                epic.start_date = convert_and_enforce_utc_timezone(
                    datetime_string=epic_dict.get("start_date")
                )
                epic.end_date = convert_and_enforce_utc_timezone(
                    datetime_string=epic_dict.get("end_date")
                )
                epic.start_date_fixed = convert_and_enforce_utc_timezone(
                    datetime_string=epic_dict.get("start_date_fixed")
                )
                epic.start_date_from_inherited_source = convert_and_enforce_utc_timezone(
                    datetime_string=epic_dict.get("start_date_from_inherited_source")
                )
                epic.due_date = convert_and_enforce_utc_timezone(
                    datetime_string=epic_dict.get("due_date")
                )
                epic.due_date_fixed = convert_and_enforce_utc_timezone(
                    datetime_string=epic_dict.get("due_date_fixed")
                )
                epic.due_date_from_inherited_source = convert_and_enforce_utc_timezone(
                    datetime_string=epic_dict.get("due_date_from_inherited_source")
                )
                epic.last_synced_at = timezone.now()

                sync_result.add_log(f"💾 About to save epic {epic_id} to database...")
                epic.save()
                sync_result.add_log(f"✓ Database save succeeded for epic {epic_id}")
                sync_result.add_success()

            except Exception as error:
                import traceback
                error_trace = traceback.format_exc()
                error_msg = f"Failed to save epic {epic_id}: {str(error)}"
                sync_result.add_failure(error_msg)
                sync_result.add_log(f"❌ {error_msg}")
                print(f"[GitLabSync] {error_msg}")
                print(f"[GitLabSync] Stack trace:\n{error_trace}")
                continue

    # Final progress update
    sync_result.update_progress(group_count, group_count, None)

    sync_result.add_log(
        f"✓ Sync complete: {sync_result.synced_count} synced, "
        f"{sync_result.skipped_count} skipped, {sync_result.failed_count} failed"
    )
    sync_result.finish()
    print(f"[GitLabSync] {sync_result}")


def gitlab_sync_epics_api(
    request: HttpRequest,
) -> JsonResponse | HttpResponse:
    """
    Sync epics from GitLab EE 17.11.6 with background job tracking.

    New functionality not present in the original git_lab app.
    Tracks epics (GitLab EE Premium/Ultimate feature) for high-level organization.

    Returns immediately with job_id for progress tracking.
    """
    job_tracker = run_sync_in_background("epics", _sync_epics_background, request)

    return JsonResponse(
        data={"success": True, "job_id": job_tracker.id, "job_type": "epics"}
    )
