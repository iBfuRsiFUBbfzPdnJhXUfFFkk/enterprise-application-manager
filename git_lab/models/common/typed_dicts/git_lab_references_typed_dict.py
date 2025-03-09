from typing import TypedDict


class GitLabReferencesTypedDict(TypedDict):
    long: str | None
    relative: str | None
    short: str | None