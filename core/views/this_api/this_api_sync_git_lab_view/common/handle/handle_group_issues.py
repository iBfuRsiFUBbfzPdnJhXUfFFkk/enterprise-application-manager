from gitlab import Gitlab
from gitlab.v4.objects import GroupIssue, Group

from core.models.sprint import Sprint
from core.views.this_api.this_api_sync_git_lab_view.common.fetch.fetch_group_issues_by_iteration_ids import fetch_group_issues_by_iteration_ids
from core.views.this_api.this_api_sync_git_lab_view.common.handle.handle_group_issue import handle_group_issue
from core.views.this_api.this_api_sync_git_lab_view.common.indicator_map import IndicatorMap


def handle_group_issues(
        current_sprint: Sprint | None = None,
        git_lab_client: Gitlab | None = None,
        git_lab_group: Group | None = None,
        indicator_map: dict[str, IndicatorMap] | None = None,
) -> dict[str, IndicatorMap] | None:
    all_group_issues: list[GroupIssue] = fetch_group_issues_by_iteration_ids(
        git_lab_client=git_lab_client,
        git_lab_group=git_lab_group,
        iteration_ids=current_sprint.iteration_ids
    ) or []
    for group_issue in all_group_issues:
        indicator_map: list[GroupIssue] | None = handle_group_issue(
            group_issue=group_issue,
            indicator_map=indicator_map,
        )
