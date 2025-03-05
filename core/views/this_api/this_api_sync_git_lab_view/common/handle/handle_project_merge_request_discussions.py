from gitlab import Gitlab
from gitlab.v4.objects import ProjectMergeRequestDiscussion, Project, \
    ProjectMergeRequest

from core.views.this_api.this_api_sync_git_lab_view.common.fetch.fetch_project_merge_requests_discussions import \
    fetch_project_merge_requests_discussions
from core.views.this_api.this_api_sync_git_lab_view.common.indicator_map import IndicatorMap, ensure_indicator_map, \
    ensure_indicator_is_in_map
from core.views.this_api.this_api_sync_git_lab_view.common.models.git_lab_api_note import GitLabApiNote
from core.views.this_api.this_api_sync_git_lab_view.common.models.git_lab_api_user import GitLabApiUser


def handle_project_merge_request_discussions(
        git_lab_client: Gitlab | None = None,
        git_lab_project: Project | None = None,
        indicator_map: IndicatorMap | None = None,
        merge_request_internal_identification_iid: int | None = None,
        project_id: int | None = None,
        project_merge_request: ProjectMergeRequest | None = None,
) -> IndicatorMap:
    indicator_map: IndicatorMap = ensure_indicator_map(indicator_map=indicator_map)
    discussions: list[ProjectMergeRequestDiscussion] | None = fetch_project_merge_requests_discussions(
        git_lab_client=git_lab_client,
        git_lab_project=git_lab_project,
        merge_request_internal_identification_iid=merge_request_internal_identification_iid,
        project_id=project_id,
        project_merge_request=project_merge_request
    )
    if discussions is None:
        return indicator_map
    for discussion in discussions:
        notes: list[GitLabApiNote] | None = discussion.attributes["notes"]
        if notes is None:
            continue
        index: int = 0
        for note in notes:
            author: GitLabApiUser | None = note["author"]
            if author is None:
                continue
            note_git_lab_user_id_int: int | None = author["id"]
            if note_git_lab_user_id_int is None:
                continue
            note_git_lab_user_id: str = str(note_git_lab_user_id_int)
            indicator_map: IndicatorMap = ensure_indicator_is_in_map(
                git_lab_user_id=note_git_lab_user_id,
                indicator_map=indicator_map
            )
            indicator_map[note_git_lab_user_id]["number_of_comments_made"] += 1
            if not note["system"]:
                indicator_map[note_git_lab_user_id]["number_of_threads_made"] += 1
            index += 1
    return indicator_map
