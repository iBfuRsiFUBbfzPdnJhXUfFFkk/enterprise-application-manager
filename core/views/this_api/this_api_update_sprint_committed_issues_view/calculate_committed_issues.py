from gitlab.base import RESTObject


def calculate_committed_issues(
        all_group_issues: list[RESTObject] | None = None,
) -> dict | None:
    if all_group_issues is None:
        return None
    committed_issues = {}
    for issue in all_group_issues:
        weight = issue.get("weight", 0) or 0  # Default weight to 0 if not set
        assignees = issue.get("assignees", [])
        for assignee in assignees:
            gitlab_username = assignee["username"]
            if gitlab_username not in committed_issues:
                committed_issues[gitlab_username] = {"count": 0, "weight": 0}
            committed_issues[gitlab_username]["count"] += 1
            committed_issues[gitlab_username]["weight"] += weight
    return committed_issues
