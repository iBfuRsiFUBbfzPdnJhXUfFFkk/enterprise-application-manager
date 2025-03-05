from gitlab.v4.objects import GroupIssue

from core.views.this_api.this_api_sync_git_lab_view.common.indicator_map import IndicatorMap, ensure_indicator_map, \
    ensure_indicator_is_in_map
from core.views.this_api.this_api_sync_git_lab_view.common.models.git_lab_api_user import GitLabApiUser


def handle_group_issue(
        group_issue: GroupIssue | None = None,
        indicator_map: IndicatorMap | None = None,
) -> IndicatorMap:
    indicator_map: IndicatorMap = ensure_indicator_map(indicator_map=indicator_map)
    if group_issue is None:
        return indicator_map
    project_id: int | None = group_issue.project_id
    if project_id is None:
        return indicator_map
    state: str | None = group_issue.state
    if state is None:
        return indicator_map
    weight: int = group_issue.weight or 0
    author: GitLabApiUser | None = group_issue.author
    if author is None:
        return indicator_map
    author_git_lab_id_int: int | None = author["id"]
    if author_git_lab_id_int is None:
        return indicator_map
    author_git_lab_id: str = str(author_git_lab_id_int)
    if author_git_lab_id is not None:
        indicator_map: IndicatorMap = ensure_indicator_is_in_map(
            git_lab_user_id=author_git_lab_id,
            indicator_map=indicator_map
        )
        indicator_map[author_git_lab_id]["number_of_issues_authored"] += 1
    assignees: list[GitLabApiUser] | None = group_issue.assignees
    if assignees is None:
        return indicator_map
    for assignee in assignees:
        assignee_git_lab_user_id_int: int | None = assignee["id"]
        if assignee_git_lab_user_id_int is None:
            continue
        assignee_git_lab_user_id: str = str(assignee_git_lab_user_id_int)
        indicator_map: IndicatorMap = ensure_indicator_is_in_map(
            git_lab_user_id=assignee_git_lab_user_id,
            indicator_map=indicator_map
        )
        indicator_map[assignee_git_lab_user_id]["number_of_issues_committed_to"] += 1
        indicator_map[assignee_git_lab_user_id]["number_of_issues_weights_committed_to"] += weight
        if state == "closed":
            indicator_map[assignee_git_lab_user_id]["number_of_issues_delivered_on"] += 1
            indicator_map[assignee_git_lab_user_id]["number_of_issues_weights_delivered_on"] += weight
            indicator_map[assignee_git_lab_user_id]["project_ids_worked_on"].append(str(project_id))
    return indicator_map
