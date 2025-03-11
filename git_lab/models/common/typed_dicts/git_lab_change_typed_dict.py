from typing import TypedDict

class GitLabChangeTypedDict(TypedDict):
    a_mode: str | None
    b_mode: str | None
    deleted_file: str | None
    diff: str | None
    generated_file: str | None
    new_file: int | None
    new_path: str | None
    old_path: str | None
    renamed_file: str | None

class GitLabMergeRequestChangeDiffRefsTypedDict(TypedDict):
    base_sha: str | None
    head_sha: str | None
    start_sha: str | None

class GitLabMergeRequestChangesTypedDict(TypedDict):
    changes: list[GitLabChangeTypedDict] | None
    changes_count: str | None
    diff_refs: GitLabMergeRequestChangeDiffRefsTypedDict | None
    id: int
    iid: int | None
    project_id: int | None
