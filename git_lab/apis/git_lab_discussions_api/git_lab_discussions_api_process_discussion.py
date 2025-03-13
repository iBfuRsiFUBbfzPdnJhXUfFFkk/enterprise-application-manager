from core.settings.common.developer import DEBUG
from git_lab.apis.git_lab_discussions_api.git_lab_discussions_api_payload import GitLabDiscussionsApiPayload
from git_lab.apis.git_lab_discussions_api.git_lab_discussions_api_process_note import \
    git_lab_discussions_api_process_note
from git_lab.models.common.typed_dicts.git_lab_discussion_typed_dict import GitLabDiscussionTypedDict
from git_lab.models.common.typed_dicts.git_lab_note_typed_dict import GitLabNoteTypedDict
from git_lab.models.git_lab_discussion import GitLabDiscussion
from git_lab.models.git_lab_merge_request import GitLabMergeRequest


def git_lab_discussions_api_process_discussion(
        discussion_dict: GitLabDiscussionTypedDict | None = None,
        model_merge_request: GitLabMergeRequest | None = None,
        payload: GitLabDiscussionsApiPayload | None = None,
) -> GitLabDiscussionsApiPayload:
    if payload is None:
        payload: GitLabDiscussionsApiPayload = {}
    if discussion_dict is None:
        return payload
    discussion_id: str = discussion_dict.get("id")
    model_discussion: GitLabDiscussion | None = GitLabDiscussion.objects.filter(id=discussion_id).first()
    if model_discussion is None:
        return payload
    if DEBUG is True:
        print(f"--------D: {discussion_id}")
    note_dicts: list[GitLabNoteTypedDict] | None = discussion_dict.get("notes")
    if note_dicts is None:
        return payload
    payload["discussions"][discussion_dict.get("id")] = {"notes": {}}
    for index, note_dict in enumerate(iter(note_dicts)):
        note_dict: GitLabNoteTypedDict = note_dict
        payload: GitLabDiscussionsApiPayload = git_lab_discussions_api_process_note(
            index=index,
            model_discussion=model_discussion,
            model_merge_request=model_merge_request,
            note_dict=note_dict,
        )
    return payload
