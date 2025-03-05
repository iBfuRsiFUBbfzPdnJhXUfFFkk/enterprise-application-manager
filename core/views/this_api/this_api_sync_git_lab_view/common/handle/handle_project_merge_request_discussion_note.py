from core.views.this_api.this_api_sync_git_lab_view.common.indicator_map import IndicatorMap, ensure_indicator_map, \
    ensure_indicator_is_in_map
from core.views.this_api.this_api_sync_git_lab_view.common.models.git_lab_api_note import GitLabApiNote
from core.views.this_api.this_api_sync_git_lab_view.common.models.git_lab_api_user import GitLabApiUser


def handle_project_merge_request_discussion_note(
        index: int | None = None,
        indicator_map: IndicatorMap | None = None,
        note: GitLabApiNote | None = None,
) -> IndicatorMap:
    indicator_map: IndicatorMap = ensure_indicator_map(indicator_map=indicator_map)
    if note is None:
        return indicator_map
    author: GitLabApiUser | None = note["author"]
    if author is None:
        return indicator_map
    note_git_lab_user_id_int: int | None = author["id"]
    if note_git_lab_user_id_int is None:
        return indicator_map
    note_git_lab_user_id: str = str(note_git_lab_user_id_int)
    indicator_map: IndicatorMap = ensure_indicator_is_in_map(
        git_lab_user_id=note_git_lab_user_id,
        indicator_map=indicator_map
    )
    indicator_map[note_git_lab_user_id]["number_of_comments_made"] += 1
    if not note["system"] and index is not None and index == 0:
        indicator_map[note_git_lab_user_id]["number_of_threads_made"] += 1
    return indicator_map
