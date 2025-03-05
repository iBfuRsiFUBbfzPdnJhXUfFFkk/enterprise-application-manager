from core.views.this_api.this_api_sync_git_lab_view.common.indicator_map import ensure_indicator_map, \
    IndicatorMap
from core.views.this_api.this_api_sync_git_lab_view.common.models.git_lab_api_change import GitLabApiChange


def handle_project_merge_request_change(
        change: GitLabApiChange | None = None,
        indicator_map: IndicatorMap | None = None,
        merge_request_author_id: str | None = None,
) -> IndicatorMap:
    indicator_map: IndicatorMap = ensure_indicator_map(indicator_map=indicator_map)
    if change is None:
        return indicator_map
    diff_text: str | None = change["diff"]
    if diff_text is None:
        return indicator_map
    for line in diff_text.splitlines():
        if line.startswith('+'):
            indicator_map[merge_request_author_id]["number_of_code_lines_added"] += 1
        elif line.startswith('-'):
            indicator_map[merge_request_author_id]["number_of_code_lines_removed"] += 1
    return indicator_map
