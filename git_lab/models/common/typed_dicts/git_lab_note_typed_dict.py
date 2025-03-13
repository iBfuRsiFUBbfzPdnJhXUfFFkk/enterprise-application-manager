from typing import TypedDict

from git_lab.models.common.typed_dicts.git_lab_user_reference_typed_dict import GitLabUserReferenceTypedDict


class GitLabNoteTypedDict(TypedDict):
    author: GitLabUserReferenceTypedDict | None
    body: str | None
    created_at: str | None
    id: int
    noteable_id: int | None
    noteable_iid: int | None
    noteable_type: str | None
    project_id: int | None
    system: bool | None
    type: str | None
    updated_at: str | None
