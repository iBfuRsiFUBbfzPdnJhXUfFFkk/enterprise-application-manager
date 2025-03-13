from typing import TypedDict, NotRequired


class GitLabDiscussionsApiPayloadNote(TypedDict):
    title: NotRequired[str | None]
    web_url: NotRequired[str | None]


class GitLabDiscussionsApiPayloadDiscussion(TypedDict):
    notes: NotRequired[dict[int, GitLabDiscussionsApiPayloadNote] | None]


class GitLabDiscussionsApiPayload(TypedDict):
    discussions: NotRequired[dict[str, GitLabDiscussionsApiPayloadDiscussion] | None]
    total_number_of_discussions_created: NotRequired[int | None]
    total_number_of_discussions_updated: NotRequired[int | None]
    total_number_of_merge_requests_not_synchronized: NotRequired[int | None]
    total_number_of_notes_created: NotRequired[int | None]
    total_number_of_notes_updated: NotRequired[int | None]

initial_git_lab_discussions_api_payload: GitLabDiscussionsApiPayload = {
    "discussions": {},
    "total_number_of_discussions_created": 0,
    "total_number_of_discussions_updated": 0,
    "total_number_of_merge_requests_not_synchronized": 0,
    "total_number_of_notes_created": 0,
    "total_number_of_notes_updated": 0,
}
