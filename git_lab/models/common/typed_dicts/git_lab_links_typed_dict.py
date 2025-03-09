from typing import TypedDict


class GitLabLinksTypedDict(TypedDict):
    cluster_agents: str | None
    events: str | None
    issues: str | None
    labels: str | None
    members: str | None
    merge_requests: str | None
    repo_branches: str | None
    self: str | None