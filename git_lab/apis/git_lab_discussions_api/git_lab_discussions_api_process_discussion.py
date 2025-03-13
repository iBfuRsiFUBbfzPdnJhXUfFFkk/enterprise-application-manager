from core.settings.common.developer import DEBUG
from git_lab.apis.git_lab_discussions_api.git_lab_discussions_api_payload import GitLabDiscussionsApiPayload, \
    initial_git_lab_discussions_api_payload
from git_lab.apis.git_lab_discussions_api.git_lab_discussions_api_process_note import \
    git_lab_discussions_api_process_note
from git_lab.models.common.typed_dicts.git_lab_discussion_typed_dict import GitLabDiscussionTypedDict
from git_lab.models.common.typed_dicts.git_lab_note_typed_dict import GitLabNoteTypedDict
from git_lab.models.git_lab_merge_request import GitLabMergeRequest
from git_lab.models.git_lab_project import GitLabProject


def git_lab_discussions_api_process_discussion(
        discussion_dict: GitLabDiscussionTypedDict | None = None,
        model_merge_request: GitLabMergeRequest | None = None,
        model_project: GitLabProject | None = None,
        payload: GitLabDiscussionsApiPayload | None = None,
) -> GitLabDiscussionsApiPayload:
    if payload is None:
        payload: GitLabDiscussionsApiPayload = initial_git_lab_discussions_api_payload
    if discussion_dict is None:
        return payload
    discussion_id: str = discussion_dict.get("id")
    if DEBUG is True:
        print(f"--------D: {discussion_id}")
    note_dicts: list[GitLabNoteTypedDict] | None = discussion_dict.get("notes")
    if note_dicts is None or len(note_dicts) == 0:
        return payload
    payload["projects"][
        model_project.id
    ]["merge_requests"][
        model_merge_request.id
    ]["discussions"][
        discussion_dict.get("id")
    ] = {
        "notes": {}
    }
    for index, note_dict in enumerate(iter(note_dicts)):
        note_dict: GitLabNoteTypedDict = note_dict
        payload: GitLabDiscussionsApiPayload = git_lab_discussions_api_process_note(
            discussion_dict=discussion_dict,
            index=index,
            model_merge_request=model_merge_request,
            note_dict=note_dict,
            payload=payload,
        )
    return payload
