from typing import TypedDict, NotRequired

from core.settings.common.developer import DEBUG
from core.utilities.convert_and_enforce_utc_timezone import convert_and_enforce_utc_timezone
from git_lab.models.common.typed_dicts.git_lab_note_typed_dict import GitLabNoteTypedDict
from git_lab.models.common.typed_dicts.git_lab_user_reference_typed_dict import GitLabUserReferenceTypedDict
from git_lab.models.git_lab_discussion import GitLabDiscussion
from git_lab.models.git_lab_merge_request import GitLabMergeRequest
from git_lab.models.git_lab_note import GitLabNote
from git_lab.models.git_lab_project import GitLabProject
from git_lab.models.git_lab_user import GitLabUser
from scrum.models.scrum_sprint import ScrumSprint


class GitLabDiscussionsApiProcessNoteReturn(TypedDict):
    did_create: NotRequired[bool | None]
    is_missing_merge_request: NotRequired[bool | None]
    model: NotRequired[GitLabNote | None]


def git_lab_discussions_api_process_note(
        index: int | None = None,
        model_discussion: GitLabDiscussion | None = None,
        model_merge_request: GitLabMergeRequest | None = None,
        note_dict: GitLabNoteTypedDict | None = None,
) -> GitLabDiscussionsApiProcessNoteReturn:
    return_object: GitLabDiscussionsApiProcessNoteReturn = {}
    if model_merge_request is None:
        if DEBUG is True:
            print("------------N: model_merge_request is None")
        return_object["is_missing_merge_request"] = True
        return return_object
    if model_discussion is None:
        if DEBUG is True:
            print("------------N: model_discussion is None")
        return return_object
    if index is None:
        if DEBUG is True:
            print("------------N: index is None")
        return return_object
    if note_dict is None:
        if DEBUG is True:
            print("------------N: note_dict is None")
        return return_object
    note_id: int | None = note_dict.get("id")
    is_system_note: bool | None = note_dict.get("system")
    body: str | None = note_dict.get("body")
    noteable_id: int | None = note_dict.get("noteable_id")
    noteable_iid: int | None = note_dict.get("noteable_iid")
    noteable_type: str | None = note_dict.get("noteable_type")
    note_type: str | None = note_dict.get("type")
    created_at: str | None = note_dict.get("created_at")
    updated_at: str | None = note_dict.get("updated_at")
    author: GitLabUserReferenceTypedDict | None = note_dict.get("author")
    web_url: str = f"{model_merge_request.web_url}#note_{note_id}"
    if note_id is None:
        return return_object
    if is_system_note:
        return return_object
    if DEBUG is True:
        print(f"------------N: {web_url}")
        print(f"------------N: {author.get('name')}")
        print(f"------------N: {author.get('username')}")
        print(f"------------N: {body}")
    get_or_create_tuple: tuple[GitLabNote, bool] = GitLabNote.objects.get_or_create(id=note_id)
    model_note: GitLabNote = get_or_create_tuple[0]
    return_object["model"] = model_note
    return_object["did_create"] = get_or_create_tuple[1]
    model_note.body = body
    model_note.noteable_id = noteable_id
    model_note.noteable_iid = noteable_iid
    model_note.noteable_type = noteable_type
    model_note.system = is_system_note
    model_note.type = note_type
    model_note.web_url = web_url
    model_note.created_at = convert_and_enforce_utc_timezone(datetime_string=created_at)
    model_note.updated_at = convert_and_enforce_utc_timezone(datetime_string=updated_at)
    model_note.discussion = model_discussion
    if author is not None:
        model_note.author = GitLabUser.objects.filter(id=author.get("id")).first()
    project: GitLabProject | None = GitLabProject.objects.filter(id=note_dict.get("project_id")).first()
    if project is not None:
        model_note.project = project
        model_discussion.project = project
        model_note.group = project.group
        model_discussion.group = project.group
    scrum_sprint: ScrumSprint | None = ScrumSprint.objects.filter(
        date_start__lte=model_note.created_at,
        date_end__gte=model_note.created_at,
    ).first()
    if scrum_sprint is not None:
        model_note.scrum_sprint = scrum_sprint
        model_discussion.scrum_sprint = scrum_sprint
    if index == 0:
        model_discussion.created_at = convert_and_enforce_utc_timezone(
            datetime_string=created_at
        )
        model_discussion.updated_at = convert_and_enforce_utc_timezone(
            datetime_string=updated_at
        )
        if author is not None:
            model_discussion.started_by = GitLabUser.objects.filter(id=author.get("id")).first()
    else:
        model_discussion.updated_at = convert_and_enforce_utc_timezone(
            datetime_string=updated_at
        )
    model_note.save()
    return return_object
