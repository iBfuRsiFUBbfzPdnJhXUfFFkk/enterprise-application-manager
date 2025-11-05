from typing import cast

from django.http import HttpRequest, HttpResponse, JsonResponse
from gitlab import Gitlab
from gitlab.v4.objects import Group, GroupSubgroup

from core.models.this_server_configuration import ThisServerConfiguration
from core.utilities.convert_and_enforce_utc_timezone import (
    convert_and_enforce_utc_timezone,
)
from core.utilities.git_lab.get_git_lab_client import get_git_lab_client
from core.views.generic.generic_500 import generic_500
from git_lab.apis.common.get_common_query_parameters import (
    GitLabApiCommonQueryParameters,
    get_common_query_parameters,
)
from gitlab_sync.models import GitLabSyncGroup, GitLabSyncJobTracker
from gitlab_sync.utilities import (
    SyncResult,
    check_job_cancelled,
    handle_gitlab_api_errors,
    run_sync_in_background,
)


def process_and_save_group(
    group: Group,
    sync_result: SyncResult,
    idx: int,
    total: int,
) -> tuple[bool, str]:
    """
    Process and save a single group, checking if it needs updating.

    Returns:
        Tuple of (needs_update, status_message)
    """
    from datetime import datetime

    from gitlab_sync.models import GitLabSyncGroup

    group_dict = group.asdict()
    group_id: int | None = group_dict.get("id")

    if group_id is None:
        return False, "skip"

    try:
        # Get or create the group
        git_lab_group, created = GitLabSyncGroup.objects.get_or_create(id=group_id)

        # Check if we need to update (new or updated since last sync)
        group_created_at = convert_and_enforce_utc_timezone(
            datetime_string=group_dict.get("created_at")
        )

        needs_update = created or (
            git_lab_group.last_synced_at is None or
            (group_created_at and group_created_at > git_lab_group.last_synced_at)
        )

        if not needs_update:
            sync_result.add_skip()
            sync_result.update_progress(
                idx, total, f"⊘ Skipped unchanged group {group_dict.get('full_path')}"
            )
            return False, "skipped"

        # Update group fields
        git_lab_group.avatar_url = group_dict.get("avatar_url")
        git_lab_group.description = group_dict.get("description")
        git_lab_group.full_name = group_dict.get("full_name")
        git_lab_group.full_path = group_dict.get("full_path")
        git_lab_group.name = group_dict.get("name")
        git_lab_group.path = group_dict.get("path")
        git_lab_group.web_url = group_dict.get("web_url")
        git_lab_group.visibility = group_dict.get("visibility")
        git_lab_group.created_at = group_created_at
        git_lab_group.last_synced_at = datetime.now()

        git_lab_group.save()
        sync_result.add_success()
        sync_result.update_progress(
            idx, total, f"✓ Synced group {git_lab_group.full_path}"
        )
        return True, "synced"

    except Exception as error:
        error_msg = f"Failed to save group {group_id}: {str(error)}"
        sync_result.add_failure(error_msg)
        sync_result.add_log(f"❌ {error_msg}")
        return False, "failed"


def recurse_groups(
    git_lab_client: Gitlab | None = None,
    parent_group: Group | None = None,
    query_parameters: GitLabApiCommonQueryParameters | None = None,
    current_depth: int = 0,
    max_depth: int = 5,
    sync_result: SyncResult | None = None,
    processed_count: list[int] | None = None,
    total_estimate: list[int] | None = None,
) -> int:
    """
    Recursively fetch and save subgroups from a parent group.

    Processes groups incrementally - saves each one immediately instead of
    accumulating in memory. This makes syncs resumable and more memory efficient.

    Args:
        git_lab_client: GitLab API client
        parent_group: Parent group to fetch subgroups from
        query_parameters: Query parameters for API calls
        current_depth: Current recursion depth (default: 0)
        max_depth: Maximum recursion depth (default: 5)
        sync_result: Sync result tracker
        processed_count: Mutable list holding current count (for tracking)
        total_estimate: Mutable list holding total estimate

    Returns:
        Number of groups processed at this level
    """
    if git_lab_client is None or parent_group is None:
        return 0
    if current_depth >= max_depth:
        return 0
    if processed_count is None:
        processed_count = [0]
    if total_estimate is None:
        total_estimate = [10]  # Initial estimate

    subgroups, error = handle_gitlab_api_errors(
        func=lambda: cast(
            list[GroupSubgroup],
            parent_group.subgroups.list(**(query_parameters or dict(all=True))),
        ),
        entity_name=f"Subgroups for {parent_group.full_path}",
        max_retries=3,
    )

    if error or not subgroups:
        return 0

    groups_at_level = 0

    for subgroup in subgroups:
        # Check if job was cancelled
        if sync_result and check_job_cancelled(sync_result.job_tracker_id):
            sync_result.add_log("⚠️ Job cancelled by user, stopping sync...")
            return groups_at_level

        child_group, error = handle_gitlab_api_errors(
            func=lambda: git_lab_client.groups.get(id=subgroup.id),
            entity_name=f"Group {subgroup.id}",
            max_retries=3,
        )

        if error or not child_group:
            continue

        # Process and save this group immediately
        processed_count[0] += 1
        total_estimate[0] = max(total_estimate[0], processed_count[0] + 5)

        if sync_result:
            process_and_save_group(
                child_group, sync_result, processed_count[0], total_estimate[0]
            )

        groups_at_level += 1

        # Recurse into subgroups
        sub_count = recurse_groups(
            git_lab_client=git_lab_client,
            parent_group=child_group,
            query_parameters=query_parameters,
            current_depth=current_depth + 1,
            max_depth=max_depth,
            sync_result=sync_result,
            processed_count=processed_count,
            total_estimate=total_estimate,
        )
        groups_at_level += sub_count

    return groups_at_level


def _sync_groups_background(
    request: HttpRequest, job_tracker: GitLabSyncJobTracker
) -> None:
    """Background function to sync groups with progress tracking."""
    sync_result = SyncResult(
        entity_type="GitLabSyncGroup", job_tracker_id=job_tracker.id
    )
    sync_result.add_log("Starting groups sync...")

    query_parameters: GitLabApiCommonQueryParameters = get_common_query_parameters(
        request=request
    )

    git_lab_client: Gitlab | None = get_git_lab_client()
    if git_lab_client is None:
        sync_result.add_log("❌ Failed to get GitLab client - check configuration")
        sync_result.add_failure("Failed to get GitLab client - check configuration")
        sync_result.finish()
        print(f"[GitLabSync] {sync_result}")
        return

    config = ThisServerConfiguration.current()
    connection_git_lab_top_level_group_id = config.connection_git_lab_top_level_group_id

    if not connection_git_lab_top_level_group_id:
        sync_result.add_log("❌ GitLab top-level group ID not configured")
        sync_result.add_failure(
            "GitLab top-level group ID not configured in ThisServerConfiguration"
        )
        sync_result.finish()
        print(f"[GitLabSync] {sync_result}")
        return

    sync_result.add_log(
        f"Fetching top-level group {connection_git_lab_top_level_group_id}..."
    )
    group_parent, error = handle_gitlab_api_errors(
        func=lambda: git_lab_client.groups.get(
            id=connection_git_lab_top_level_group_id
        ),
        entity_name=f"Top-level group {connection_git_lab_top_level_group_id}",
        max_retries=3,
    )

    if error or not group_parent:
        sync_result.add_log(f"❌ Failed to fetch top-level group: {error}")
        sync_result.add_failure(
            f"Failed to fetch top-level group: {error or 'Group not found'}"
        )
        sync_result.finish()
        print(f"[GitLabSync] {sync_result}")
        return

    max_depth = config.coerced_gitlab_sync_max_group_depth
    sync_result.add_log(
        f"✓ Fetched top-level group, recursing and syncing subgroups incrementally (max depth: {max_depth})..."
    )

    # Process the parent group first
    from datetime import datetime

    from gitlab_sync.models import GitLabSyncGroup

    processed_count = [0]
    total_estimate = [10]

    parent_dict = group_parent.asdict()
    parent_id = parent_dict.get("id")

    if parent_id:
        processed_count[0] += 1
        git_lab_group, created = GitLabSyncGroup.objects.get_or_create(id=parent_id)

        # Check if we need to update
        parent_created_at = convert_and_enforce_utc_timezone(
            datetime_string=parent_dict.get("created_at")
        )

        needs_update = created or (
            git_lab_group.last_synced_at is None
            or (parent_created_at and parent_created_at > git_lab_group.last_synced_at)
        )

        if needs_update:
            git_lab_group.avatar_url = parent_dict.get("avatar_url")
            git_lab_group.description = parent_dict.get("description")
            git_lab_group.full_name = parent_dict.get("full_name")
            git_lab_group.full_path = parent_dict.get("full_path")
            git_lab_group.name = parent_dict.get("name")
            git_lab_group.path = parent_dict.get("path")
            git_lab_group.web_url = parent_dict.get("web_url")
            git_lab_group.visibility = parent_dict.get("visibility")
            git_lab_group.created_at = parent_created_at
            git_lab_group.last_synced_at = datetime.now()
            git_lab_group.save()
            sync_result.add_success()
            sync_result.add_log(f"✓ Synced top-level group {git_lab_group.full_path}")
        else:
            sync_result.add_skip()
            sync_result.add_log(
                f"⊘ Skipped unchanged top-level group {parent_dict.get('full_path')}"
            )

    # Check if job was cancelled before recursing
    if check_job_cancelled(sync_result.job_tracker_id):
        sync_result.add_log("⚠️ Job cancelled by user, stopping sync...")
        sync_result.finish()
        print(f"[GitLabSync] {sync_result}")
        return

    # Recursively process subgroups (they save immediately)
    recurse_groups(
        git_lab_client=git_lab_client,
        parent_group=group_parent,
        query_parameters=query_parameters,
        current_depth=0,
        max_depth=max_depth,
        sync_result=sync_result,
        processed_count=processed_count,
        total_estimate=total_estimate,
    )

    sync_result.add_log(
        f"✓ Sync complete: {sync_result.synced_count} synced, "
        f"{sync_result.skipped_count} skipped, {sync_result.failed_count} failed"
    )
    sync_result.finish()
    print(f"[GitLabSync] {sync_result}")


def gitlab_sync_groups_api(
    request: HttpRequest,
) -> JsonResponse | HttpResponse:
    """
    Sync GitLab groups from GitLab EE 17.11.6 with background job tracking.

    This is the FIRST endpoint to call - it syncs the top-level group and all
    subgroups. Projects sync depends on groups existing first.

    Returns immediately with job_id for progress tracking.
    """
    job_tracker = run_sync_in_background("groups", _sync_groups_background, request)

    return JsonResponse(
        data={"success": True, "job_id": job_tracker.id, "job_type": "groups"}
    )
