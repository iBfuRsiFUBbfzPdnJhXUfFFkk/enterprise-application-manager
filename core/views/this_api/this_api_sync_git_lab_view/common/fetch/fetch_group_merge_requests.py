from typing import cast

from gitlab import Gitlab
from gitlab.v4.objects import Group, GroupMergeRequest

from core.models.sprint import Sprint
from core.views.this_api.this_api_sync_git_lab_view.common.fetch.fetch_git_lab_group import fetch_git_lab_group


def fetch_group_merge_requests(
        current_sprint: Sprint | None = None,
        git_lab_client: Gitlab | None = None,
        git_lab_group: Group | None = None,
) -> list[GroupMergeRequest] | None:
    if current_sprint is None:
        current_sprint: Sprint | None = Sprint.current_sprint()
    if fetch_git_lab_group is None:
        git_lab_group: Group | None = fetch_git_lab_group(git_lab_client=git_lab_client)
    if git_lab_group is None:
        return None
    return cast(
        typ=list[GroupMergeRequest],
        val=git_lab_group.mergerequests.list(
            get_all=True,
            lazy=True,
            state="merged",
            updated_after=current_sprint.date_start.isoformat(),
            updated_before=current_sprint.date_end.isoformat(),
        )
    )
