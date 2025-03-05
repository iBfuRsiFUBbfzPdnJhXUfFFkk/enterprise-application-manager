from gitlab import Gitlab
from gitlab.v4.objects import Group, GroupMember

from core.utilities.git_lab.get_git_lab_client import get_git_lab_client
from core.views.this_api.this_api_sync_git_lab_view.common.fetch.fetch_git_lab_group import fetch_git_lab_group
from core.views.this_api.this_api_sync_git_lab_view.common.fetch.fetch_group_users import fetch_group_users
from core.views.this_api.this_api_sync_git_lab_view.common.handle.handle_group_member import handle_group_member
from core.views.this_api.this_api_sync_git_lab_view.common.indicator_map import IndicatorMap, ensure_indicator_map


def handle_group_members(
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
    group_members: list[GroupMember] | None = fetch_group_users(
        git_lab_client=git_lab_client,
        git_lab_group=git_lab_group,
    )
    if group_members is None:
        return indicator_map
    for group_member in group_members:
        indicator_map: IndicatorMap = handle_group_member(
            group_member=group_member,
            indicator_map=indicator_map,
        )
    return indicator_map
