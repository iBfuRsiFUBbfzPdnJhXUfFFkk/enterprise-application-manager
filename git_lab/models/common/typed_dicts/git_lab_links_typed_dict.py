from typing import TypedDict


class GitLabLinksTypedDict(TypedDict):
    award_emoji: str | None # issue only
    cluster_agents: str | None # project only
    events: str | None # project only
    issues: str | None # project only
    labels: str | None # project only
    members: str | None # project only
    notes: str | None # issue only
    merge_requests: str | None # project only
    project: str | None # issue only
    repo_branches: str | None # project only
    self: str | None