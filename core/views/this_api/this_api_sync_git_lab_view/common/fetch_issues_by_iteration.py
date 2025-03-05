from typing import cast

from gitlab import Gitlab
from gitlab.v4.objects import Group, GroupIssue

from core.views.this_api.this_api_sync_git_lab_view.common.get_git_lab_group import get_git_lab_group


def fetch_issues_by_iteration(
        git_lab_client: Gitlab | None = None,
        git_lab_group: Group | None = None,
        iteration_id: int | str | None = None,
) -> list[GroupIssue] | None:
    if get_git_lab_group is None:
        git_lab_group: Group | None = get_git_lab_group(git_lab_client=git_lab_client)
    if git_lab_group is None:
        return None
    return cast(
        typ=list[GroupIssue],
        val=git_lab_group.issues.list(
            get_all=True,
            iteration_id=iteration_id,
            state="all",
        )
    )
