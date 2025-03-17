from typing import TypedDict


class GitLabMergeRequestChangeDiffRefsTypedDict(TypedDict):
    base_sha: str | None
    head_sha: str | None
    start_sha: str | None
