from typing import TypedDict


class GitLabReferencesTypedDict(TypedDict):
    full: str | None # issue uses this instead of long
    long: str | None
    relative: str | None
    short: str | None