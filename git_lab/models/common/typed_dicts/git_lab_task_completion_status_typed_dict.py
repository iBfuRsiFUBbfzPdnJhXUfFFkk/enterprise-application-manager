from typing import TypedDict


class GitLabTaskCompletionStatusTypedDict(TypedDict):
    completed_count: int | None
    count: int | None