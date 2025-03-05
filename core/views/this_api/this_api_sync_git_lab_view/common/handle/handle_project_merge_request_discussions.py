from typing import TypedDict

from gitlab import Gitlab
from gitlab.v4.objects import ProjectMergeRequestDiscussion, Project, \
    ProjectMergeRequest

from core.views.this_api.this_api_sync_git_lab_view.common.fetch.fetch_project_merge_requests_discussions import \
    fetch_project_merge_requests_discussions
from core.views.this_api.this_api_sync_git_lab_view.common.indicator_map import IndicatorMap, create_initial_indicator_map


class GitLabNoteAuthor(TypedDict):
    username: str | None


class GitLabNote(TypedDict):
    author: GitLabNoteAuthor | None
    system: bool | None


def handle_project_merge_request_discussions(
        git_lab_client: Gitlab | None = None,
        git_lab_project: Project | None = None,
        indicator_map: dict[str, IndicatorMap] | None = None,
        merge_request_internal_identification_iid: int | None = None,
        project_id: int | None = None,
        project_merge_request: ProjectMergeRequest | None = None,
) -> dict[str, IndicatorMap]:
    if indicator_map is None:
        indicator_map: dict[str, IndicatorMap] = {}
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
        notes: list[GitLabNote] | None = discussion.attributes["notes"]
        if notes is None:
            continue
        index: int = 0
        for note in notes:
            author: GitLabNoteAuthor | None = note["author"]
            if author is None:
                continue
            note_username: str | None = author["username"]
            if note_username is None:
                continue
            if note_username not in indicator_map:
                indicator_map[note_username] = create_initial_indicator_map()
            indicator_map[note_username]["number_of_comments_made"] += 1
            if not note["system"]:
                indicator_map[note_username]["number_of_threads_made"] += 1
            index += 1
    return indicator_map
