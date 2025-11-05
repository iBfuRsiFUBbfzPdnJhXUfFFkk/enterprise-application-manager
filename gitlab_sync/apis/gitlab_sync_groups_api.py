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
    handle_gitlab_api_errors,
    run_sync_in_background,
)


def recurse_groups(
    all_groups: set[Group] | None = None,
    git_lab_client: Gitlab | None = None,
    parent_group: Group | None = None,
    query_parameters: GitLabApiCommonQueryParameters | None = None,
) -> set[Group]:
    """
    Recursively fetch all subgroups from a parent group.

    Args:
        all_groups: Set of already collected groups
        git_lab_client: GitLab API client
        parent_group: Parent group to fetch subgroups from
        query_parameters: Query parameters for API calls

    Returns:
        Set of all groups (parent + all subgroups)
    """
    if all_groups is None:
        all_groups = set()
    if git_lab_client is None:
        return all_groups
    if parent_group is None:
        return all_groups

    subgroups, error = handle_gitlab_api_errors(
        func=lambda: cast(
            list[GroupSubgroup],
            parent_group.subgroups.list(**(query_parameters or dict(all=True))),
        ),
        entity_name=f"Subgroups for {parent_group.full_path}",
        max_retries=3,
    )

    if error or not subgroups:
        return all_groups

    for subgroup in subgroups:
        child_group, error = handle_gitlab_api_errors(
            func=lambda: git_lab_client.groups.get(id=subgroup.id),
            entity_name=f"Group {subgroup.id}",
            max_retries=3,
        )

        if error or not child_group:
            continue

        all_groups.add(child_group)
        all_groups = recurse_groups(
            all_groups=all_groups,
            git_lab_client=git_lab_client,
            parent_group=child_group,
            query_parameters=query_parameters,
        )

    return all_groups


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

    sync_result.add_log("✓ Fetched top-level group, recursing subgroups...")
    all_groups: set[Group] = recurse_groups(
        all_groups={group_parent},
        git_lab_client=git_lab_client,
        parent_group=group_parent,
        query_parameters=query_parameters,
    )

    group_dicts: list[dict] = [group.asdict() for group in list(all_groups)]
    total_groups = len(group_dicts)
    sync_result.add_log(f"✓ Found {total_groups} groups to sync")
    sync_result.update_progress(0, total_groups)

    for idx, group_dict in enumerate(group_dicts, 1):
        group_id: int | None = group_dict.get("id")
        if group_id is None:
            sync_result.add_skip()
            continue

        try:
            git_lab_group, created = GitLabSyncGroup.objects.get_or_create(id=group_id)

            git_lab_group.avatar_url = group_dict.get("avatar_url")
            git_lab_group.description = group_dict.get("description")
            git_lab_group.full_name = group_dict.get("full_name")
            git_lab_group.full_path = group_dict.get("full_path")
            git_lab_group.name = group_dict.get("name")
            git_lab_group.path = group_dict.get("path")
            git_lab_group.web_url = group_dict.get("web_url")
            git_lab_group.visibility = group_dict.get("visibility")

            git_lab_group.created_at = convert_and_enforce_utc_timezone(
                datetime_string=group_dict.get("created_at")
            )

            git_lab_group.save()
            sync_result.add_success()
            sync_result.update_progress(
                idx, total_groups, f"✓ Synced group {git_lab_group.full_path}"
            )

        except Exception as error:
            error_msg = f"Failed to save group {group_id}: {str(error)}"
            sync_result.add_failure(error_msg)
            sync_result.add_log(f"❌ {error_msg}")
            continue

    sync_result.add_log(
        f"✓ Sync complete: {sync_result.synced_count} synced, {sync_result.failed_count} failed"
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
