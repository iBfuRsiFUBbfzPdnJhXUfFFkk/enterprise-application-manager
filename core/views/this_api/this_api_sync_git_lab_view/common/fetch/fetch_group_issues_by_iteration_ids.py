from gitlab import Gitlab
from gitlab.v4.objects import Group, GroupIssue

from core.views.this_api.this_api_sync_git_lab_view.common.fetch.fetch_group_issues_by_iteration_id import \
    fetch_group_issues_by_iteration_id


def fetch_group_issues_by_iteration_ids(
        git_lab_client: Gitlab | None = None,
        git_lab_group: Group | None = None,
        iteration_ids: list[int | str] | None = None,
) -> list[GroupIssue] | None:
    if iteration_ids is None:
        return None
    all_group_issues: list[GroupIssue] = []
    for iteration_id in iteration_ids:
        group_issues: list[GroupIssue] | None = fetch_group_issues_by_iteration_id(
            git_lab_client=git_lab_client,
            git_lab_group=git_lab_group,
            iteration_id=iteration_id
        )
        if group_issues is None:
            continue
        all_group_issues.extend(group_issues)
    return all_group_issues
