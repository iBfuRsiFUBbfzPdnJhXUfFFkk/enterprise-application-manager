from core.views.this_api.this_api_sync_git_lab_view.common.indicator_map import ensure_indicator_map, IndicatorMap, \
    ensure_indicator_is_in_map
from core.views.this_api.this_api_sync_git_lab_view.common.models.git_lab_api_user import GitLabApiUser


def handle_project_merge_request_approval(
        approval: GitLabApiUser | None = None,
        indicator_map: IndicatorMap | None = None,
) -> IndicatorMap:
    indicator_map: IndicatorMap = ensure_indicator_map(indicator_map=indicator_map)
    if approval is None:
        return indicator_map
    approved_by_git_lab_user_id_int: int | None = approval["id"]
    if approved_by_git_lab_user_id_int is None:
        return indicator_map
    approved_by_git_lab_user_id: str = str(approved_by_git_lab_user_id_int)
    indicator_map: IndicatorMap = ensure_indicator_is_in_map(
        git_lab_user_id=approved_by_git_lab_user_id,
        indicator_map=indicator_map
    )
    indicator_map[approved_by_git_lab_user_id]["number_of_approvals"] += 1
    return indicator_map
