from typing import TypedDict


class GitLabChangeTypedDict(TypedDict):
    a_mode: str | None
    b_mode: str | None
    deleted_file: bool | None
    diff: str | None
    generated_file: bool | None
    new_file: bool | None
    new_path: str | None
    old_path: str | None
    renamed_file: bool | None
