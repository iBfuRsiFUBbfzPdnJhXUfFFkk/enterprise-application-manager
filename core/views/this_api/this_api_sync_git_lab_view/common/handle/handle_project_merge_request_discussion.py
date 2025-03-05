from gitlab.v4.objects import ProjectMergeRequestDiscussion

from core.views.this_api.this_api_sync_git_lab_view.common.handle.handle_project_merge_request_discussion_note import \
    handle_project_merge_request_discussion_note
from core.views.this_api.this_api_sync_git_lab_view.common.indicator_map import IndicatorMap, ensure_indicator_map
from core.views.this_api.this_api_sync_git_lab_view.common.models.git_lab_api_note import GitLabApiNote


def handle_project_merge_request_discussion(
        discussion: ProjectMergeRequestDiscussion | None = None,
        indicator_map: IndicatorMap | None = None,
) -> IndicatorMap:
    indicator_map: IndicatorMap = ensure_indicator_map(indicator_map=indicator_map)
    if discussion is None:
        return indicator_map
    notes: list[GitLabApiNote] | None = discussion.attributes["notes"]
    if notes is None:
        return indicator_map
    index: int = 0
    for note in notes:
        indicator_map: IndicatorMap = handle_project_merge_request_discussion_note(
            index=index,
            indicator_map=indicator_map,
            note=note,
        )
        index += 1
    return indicator_map
