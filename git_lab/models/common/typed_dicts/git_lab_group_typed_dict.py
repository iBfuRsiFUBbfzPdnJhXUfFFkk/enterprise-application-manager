from typing import TypedDict


class GitLabGroupTypedDict(TypedDict):
    avatar_url: str | None
    created_at: str | None
    description: str | None
    full_name: str | None
    full_path: str | None
    id: int
    name: str | None
    path: str | None
    web_url: str | None