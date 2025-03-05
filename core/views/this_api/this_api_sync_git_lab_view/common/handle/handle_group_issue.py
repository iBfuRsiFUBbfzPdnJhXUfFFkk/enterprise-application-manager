from typing import TypedDict

from gitlab.v4.objects import GroupIssue

from core.views.this_api.this_api_sync_git_lab_view.common.indicator_map import IndicatorMap, create_initial_indicator_map


class GroupIssueUser(TypedDict):
    username: str | None


def handle_group_issue(
        group_issue: GroupIssue | None = None,
        indicator_map: dict[str, IndicatorMap] | None = None,
) -> dict[str, IndicatorMap] | None:
    if group_issue is None:
        return None
    if indicator_map is None:
        indicator_map: dict[str, IndicatorMap] = {}
    project_id: int | None = group_issue.project_id
    if project_id is None:
        return indicator_map
    state: str | None = group_issue.state
    if state is None:
        return indicator_map
    weight: int = group_issue.weight or 0
    author: GroupIssueUser | None = group_issue.author
    if author is None:
        return indicator_map
    author_username: str | None = author["username"]
    if author_username is not None:
        if author_username not in indicator_map:
            indicator_map[author_username] = create_initial_indicator_map()
        indicator_map[author_username]["number_of_issues_authored"] += 1
    assignees: list[GroupIssueUser] | None = group_issue.assignees
    if assignees is None:
        return indicator_map
    for assignee in assignees:
        assignee_username: str | None = assignee["username"]
        if assignee_username is None:
            continue
        if assignee_username not in indicator_map:
            indicator_map[assignee_username] = create_initial_indicator_map()
        indicator_map[assignee_username]["number_of_issues_committed_to"] += 1
        indicator_map[assignee_username]["number_of_issues_weights_committed_to"] += weight
        if state == "closed":
            indicator_map[assignee_username]["number_of_issues_delivered_on"] += 1
            indicator_map[assignee_username]["number_of_issues_weights_delivered_on"] += weight
            indicator_map[assignee_username]["project_ids_worked_on"].append(str(project_id))
    return indicator_map
