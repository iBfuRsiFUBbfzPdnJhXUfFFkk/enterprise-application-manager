from typing import TypedDict


class GitLabTimeStatsTypedDict(TypedDict):
    human_time_estimate: str | None
    human_total_time_spent: str | None
    time_estimate: int | None
    total_time_spent: int | None