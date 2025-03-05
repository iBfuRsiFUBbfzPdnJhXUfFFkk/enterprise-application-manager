from typing import TypedDict


class GitLabApiUser(TypedDict):
    id: int | None
    username: str | None