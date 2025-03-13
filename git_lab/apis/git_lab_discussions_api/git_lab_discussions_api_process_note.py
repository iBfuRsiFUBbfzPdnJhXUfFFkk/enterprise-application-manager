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
    model: NotRequired[GitLabNote | None]


def git_lab_discussions_api_process_note(
        model_merge_request: GitLabMergeRequest,
        git_lab_discussion: GitLabDiscussion,
        index: int,
        note_dict: GitLabNoteTypedDict,
) -> GitLabDiscussionsApiProcessNoteReturn:
    return_object: GitLabDiscussionsApiProcessNoteReturn = {}
    note_id: int | None = note_dict.get("id")
    is_system_note: bool | None = note_dict.get("system")
    body: str | None = note_dict.get("body")
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
    git_lab_note: GitLabNote = get_or_create_tuple[0]
    return_object["model"] = git_lab_note
    return_object["did_create"] = get_or_create_tuple[1]
    git_lab_note.body = note_dict.get("body")
    git_lab_note.noteable_id = note_dict.get("noteable_id")
    git_lab_note.noteable_iid = note_dict.get("noteable_iid")
    git_lab_note.noteable_type = note_dict.get("noteable_type")
    git_lab_note.system = note_dict.get("system")
    git_lab_note.type = note_dict.get("type")
    git_lab_note.created_at = convert_and_enforce_utc_timezone(datetime_string=note_dict.get("created_at"))
    git_lab_note.updated_at = convert_and_enforce_utc_timezone(datetime_string=note_dict.get("updated_at"))
    git_lab_note.discussion = git_lab_discussion
    author: GitLabUserReferenceTypedDict | None = note_dict.get("author")
    if author is not None:
        git_lab_note.author = GitLabUser.objects.filter(id=author.get("id")).first()
    project: GitLabProject | None = GitLabProject.objects.filter(id=note_dict.get("project_id")).first()
    if project is not None:
        git_lab_note.project = project
        git_lab_discussion.project = project
        git_lab_note.group = project.group
        git_lab_discussion.group = project.group
    scrum_sprint: ScrumSprint | None = ScrumSprint.objects.filter(
        date_start__lte=git_lab_note.created_at,
        date_end__gte=git_lab_note.created_at,
    ).first()
    if scrum_sprint is not None:
        git_lab_note.scrum_sprint = scrum_sprint
        git_lab_discussion.scrum_sprint = scrum_sprint
    if index == 0:
        git_lab_discussion.created_at = convert_and_enforce_utc_timezone(
            datetime_string=note_dict.get("created_at")
        )
        git_lab_discussion.updated_at = convert_and_enforce_utc_timezone(
            datetime_string=note_dict.get("updated_at")
        )
        if author is not None:
            git_lab_discussion.started_by = GitLabUser.objects.filter(id=author.get("id")).first()
    else:
        git_lab_discussion.updated_at = convert_and_enforce_utc_timezone(
            datetime_string=note_dict.get("updated_at")
        )
    git_lab_note.save()
    return return_object
