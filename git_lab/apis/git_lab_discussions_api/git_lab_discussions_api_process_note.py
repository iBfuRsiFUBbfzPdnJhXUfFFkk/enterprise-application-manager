from datetime import datetime

from core.settings.common.developer import DEBUG
from core.utilities.convert_and_enforce_utc_timezone import convert_and_enforce_utc_timezone
from git_lab.apis.git_lab_discussions_api.git_lab_discussions_api_payload import GitLabDiscussionsApiPayload, \
    initial_git_lab_discussions_api_payload
from git_lab.models.common.typed_dicts.git_lab_discussion_typed_dict import GitLabDiscussionTypedDict
from git_lab.models.common.typed_dicts.git_lab_note_typed_dict import GitLabNoteTypedDict
from git_lab.models.common.typed_dicts.git_lab_user_reference_typed_dict import GitLabUserReferenceTypedDict
from git_lab.models.git_lab_discussion import GitLabDiscussion
from git_lab.models.git_lab_merge_request import GitLabMergeRequest
from git_lab.models.git_lab_note import GitLabNote
from git_lab.models.git_lab_project import GitLabProject
from git_lab.models.git_lab_user import GitLabUser
from scrum.models.scrum_sprint import ScrumSprint


def git_lab_discussions_api_process_note(
        discussion_dict: GitLabDiscussionTypedDict | None = None,
        index: int | None = None,
        model_merge_request: GitLabMergeRequest | None = None,
        note_dict: GitLabNoteTypedDict | None = None,
        payload: GitLabDiscussionsApiPayload | None = None,
) -> GitLabDiscussionsApiPayload:
    if payload is None:
        payload: GitLabDiscussionsApiPayload = initial_git_lab_discussions_api_payload
    if model_merge_request is None:
        return payload
    if discussion_dict is None:
        if DEBUG is True:
            print("------------N: discussion_dict is None")
        return payload
    if index is None:
        if DEBUG is True:
            print("------------N: index is None")
        return payload
    if note_dict is None:
        if DEBUG is True:
            print("------------N: note_dict is None")
        return payload
    note_id: int | None = note_dict.get("id")
    if note_id is None:
        if DEBUG is True:
            print("------------N: note_id is None")
        return payload
    is_system_note: bool | None = note_dict.get("system")
    if is_system_note is True:
        if DEBUG is True:
            print("------------N: skipping system note")
        return payload
    body: str | None = note_dict.get("body")
    created_at: str | None = note_dict.get("created_at")
    note_type: str | None = note_dict.get("type")
    noteable_id: int | None = note_dict.get("noteable_id")
    noteable_iid: int | None = note_dict.get("noteable_iid")
    noteable_type: str | None = note_dict.get("noteable_type")
    updated_at: str | None = note_dict.get("updated_at")
    author: GitLabUserReferenceTypedDict | None = note_dict.get("author")
    author_id: int | None = author.get("id") if author is not None else None
    project_id: int | None = note_dict.get("project_id")
    created_at_datetime: datetime | None = convert_and_enforce_utc_timezone(datetime_string=created_at)
    updated_at_datetime: datetime | None = convert_and_enforce_utc_timezone(datetime_string=updated_at)
    model_author: GitLabUser | None = GitLabUser.objects.filter(id=author_id).first()
    model_project: GitLabProject | None = GitLabProject.objects.filter(id=project_id).first()
    model_scrum_sprint: ScrumSprint | None = ScrumSprint.objects.filter(
        date_start__lte=created_at_datetime,
        date_end__gte=created_at_datetime,
    ).first()
    title: str = f"{author.get('username')} on {model_merge_request.title} for {model_project}"
    web_url: str = f"{model_merge_request.web_url}#note_{note_id}"
    if DEBUG is True:
        print(f"------------N: {web_url}")
        print(f"------------N: {author.get('name')}")
        print(f"------------N: {author.get('username')}")
        print(f"------------N: {body}")
    discussion_id: str = discussion_dict.get("id")
    get_or_create_tuple: tuple[GitLabDiscussion, bool] = GitLabDiscussion.objects.get_or_create(id=discussion_id)
    model_discussion: GitLabDiscussion = get_or_create_tuple[0]
    did_create: bool = get_or_create_tuple[1]
    if did_create is True:
        payload["total_number_of_discussions_created"] += 1
    else:
        payload["total_number_of_discussions_updated"] += 1
    model_discussion.individual_note = discussion_dict.get("individual_note")
    get_or_create_tuple: tuple[GitLabNote, bool] = GitLabNote.objects.get_or_create(id=note_id)
    model_note: GitLabNote = get_or_create_tuple[0]
    did_create: bool = get_or_create_tuple[1]
    if did_create is True:
        payload["total_number_of_notes_created"] += 1
    else:
        payload["total_number_of_notes_updated"] += 1
    payload["projects"][
        project_id
    ]["merge_requests"][
        model_merge_request.id
    ]["discussions"][
        model_discussion.id
    ]["notes"][
        note_id
    ] = {
        "title": title,
        "web_url": web_url,
    }
    model_discussion.group = model_project.group
    model_discussion.project = model_project
    model_discussion.scrum_sprint = model_scrum_sprint
    model_discussion.updated_at = updated_at_datetime
    model_note.author = model_author
    model_note.body = body
    model_note.created_at = created_at_datetime
    model_note.discussion = model_discussion
    model_note.group = model_project.group
    model_note.noteable_id = noteable_id
    model_note.noteable_iid = noteable_iid
    model_note.noteable_type = noteable_type
    model_note.project = model_project
    model_note.scrum_sprint = model_scrum_sprint
    model_note.system = is_system_note
    model_note.title = title
    model_note.type = note_type
    model_note.updated_at = updated_at_datetime
    model_note.web_url = web_url
    if index == 0:
        model_discussion.created_at = created_at_datetime
        model_discussion.started_by = model_author
    model_note.save()
    model_discussion.save()
    return payload
