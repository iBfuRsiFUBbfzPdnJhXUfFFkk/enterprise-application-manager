from gitlab import Gitlab
from gitlab.v4.objects import GroupMergeRequest, Group

from core.models.sprint import Sprint
from core.utilities.git_lab.get_git_lab_client import get_git_lab_client
from core.views.this_api.this_api_sync_git_lab_view.common.fetch.fetch_git_lab_group import fetch_git_lab_group
from core.views.this_api.this_api_sync_git_lab_view.common.fetch.fetch_group_merge_requests import \
    fetch_group_merge_requests
from core.views.this_api.this_api_sync_git_lab_view.common.handle.handle_group_merge_request import \
    handle_group_merge_request
from core.views.this_api.this_api_sync_git_lab_view.common.indicator_map import IndicatorMap, \
    ensure_indicator_map


def handle_group_merge_requests(
        current_sprint: Sprint | None = None,
        git_lab_client: Gitlab | None = None,
        git_lab_group: Group | None = None,
        indicator_map: IndicatorMap | None = None,
) -> IndicatorMap:
    indicator_map: IndicatorMap = ensure_indicator_map(indicator_map=indicator_map)
    if git_lab_client is None:
        git_lab_client: Gitlab | None = get_git_lab_client()
    if git_lab_client is None:
        return indicator_map
    if git_lab_group is None:
        git_lab_group: Group | None = fetch_git_lab_group(git_lab_client=git_lab_client)
    if git_lab_group is None:
        return indicator_map
    if current_sprint is None:
        current_sprint: Sprint | None = Sprint.current_sprint()
    if current_sprint is None:
        return indicator_map
    all_group_merge_requests: list[GroupMergeRequest] | None = fetch_group_merge_requests(
        current_sprint=current_sprint,
        git_lab_client=git_lab_client,
        git_lab_group=git_lab_group,
    )
    if all_group_merge_requests is None:
        return indicator_map
    for group_merge_request in all_group_merge_requests:
        indicator_map: IndicatorMap = handle_group_merge_request(
            git_lab_client=git_lab_client,
            group_merge_request=group_merge_request,
            indicator_map=indicator_map,
        )
    return indicator_map
