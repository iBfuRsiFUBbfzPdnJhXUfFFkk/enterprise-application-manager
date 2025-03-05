from gitlab import Gitlab
from gitlab.v4.objects import Group, GroupIssue

from core.views.this_api.this_api_sync_git_lab_view.common.fetch_issues_by_iteration import \
    fetch_issues_by_iteration


def fetch_issues_by_iterations(
        git_lab_client: Gitlab | None = None,
        git_lab_group: Group | None = None,
        iteration_ids: list[int | str] | None = None,
) -> list[GroupIssue] | None:
    if iteration_ids is None:
        return None
    all_group_issues: list[GroupIssue] = []
    for iteration_id in iteration_ids:
        all_group_issues.extend(fetch_issues_by_iteration(
            git_lab_client=git_lab_client,
            git_lab_group=git_lab_group,
            iteration_id=iteration_id
        ) or [])
    return all_group_issues
