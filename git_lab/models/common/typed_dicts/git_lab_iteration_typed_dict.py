from typing import TypedDict


class GitLabIterationTypedDict(TypedDict):
    created_at: str | None
    description: str | None
    due_date: str | None
    group_id: int | None
    id: int
    iid: int | None
    sequence: int | None
    start_date: str | None
    state: int | None
    title: str | None
    updated_at: str | None
    web_url: str | None
