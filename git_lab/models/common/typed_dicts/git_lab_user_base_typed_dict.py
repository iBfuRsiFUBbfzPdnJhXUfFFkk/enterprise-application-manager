from typing import TypedDict


class GitLabUserBaseTypedDict(TypedDict):
    avatar_url: str | None
    id: int | None
    locked: bool | None
    name: str | None
    username: str | None
    web_url: str | None