from typing import TypedDict

from git_lab.models.common.typed_dicts.git_lab_note_typed_dict import GitLabNoteTypedDict


class GitLabDiscussionTypedDict(TypedDict):
    id: str | None  # this is string of characters
    individual_note: bool | None
    notes: list[GitLabNoteTypedDict] | None
