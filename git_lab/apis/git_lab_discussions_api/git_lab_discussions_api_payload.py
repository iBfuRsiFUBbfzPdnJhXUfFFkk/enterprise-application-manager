from typing import TypedDict, NotRequired


class GitLabDiscussionsApiPayload(TypedDict):
    total_number_of_discussions_created: NotRequired[int | None]
    total_number_of_discussions_updated: NotRequired[int | None]
    total_number_of_merge_requests_not_synchronized: NotRequired[int | None]
    total_number_of_notes_created: NotRequired[int | None]
    total_number_of_notes_updated: NotRequired[int | None]
    total_number_of_projects_denied_access: NotRequired[int | None]
    total_number_of_system_notes_skipped: NotRequired[int | None]


initial_git_lab_discussions_api_payload: GitLabDiscussionsApiPayload = {
    "total_number_of_discussions_created": 0,
    "total_number_of_discussions_updated": 0,
    "total_number_of_merge_requests_not_synchronized": 0,
    "total_number_of_notes_created": 0,
    "total_number_of_notes_updated": 0,
    "total_number_of_projects_denied_access": 0,
    "total_number_of_system_notes_skipped": 0,
}
