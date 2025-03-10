from gitlab import Gitlab
from gitlab.v4.objects import GroupIssue, Group

from core.models.sprint import Sprint
from core.views.this_api.this_api_sync_git_lab_view.common.fetch.fetch_group_issues_by_iteration_ids import \
    fetch_group_issues_by_iteration_ids
from core.views.this_api.this_api_sync_git_lab_view.common.handle.handle_group_issue import handle_group_issue
from core.views.this_api.this_api_sync_git_lab_view.common.indicator_map import IndicatorMap, \
    ensure_indicator_map


def handle_group_issues(
        current_sprint: Sprint | None = None,
        git_lab_client: Gitlab | None = None,
        git_lab_group: Group | None = None,
        indicator_map: IndicatorMap | None = None,
) -> IndicatorMap:
    indicator_map: IndicatorMap = ensure_indicator_map(indicator_map=indicator_map)
    all_group_issues: list[GroupIssue] | None = fetch_group_issues_by_iteration_ids(
        git_lab_client=git_lab_client,
        git_lab_group=git_lab_group,
        iteration_ids=current_sprint.git_lab_iteration_ids
    )
    if all_group_issues is None:
        return indicator_map
    for group_issue in all_group_issues:
        indicator_map: IndicatorMap = handle_group_issue(
            group_issue=group_issue,
            indicator_map=indicator_map,
        )
    return indicator_map
