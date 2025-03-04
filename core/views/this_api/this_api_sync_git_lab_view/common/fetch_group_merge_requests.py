from typing import cast

from gitlab.v4.objects import Group, GroupMergeRequest

from core.models.sprint import Sprint
from core.views.this_api.this_api_sync_git_lab_view.common.get_git_lab_group import get_git_lab_group


def fetch_group_merge_requests() -> list[GroupMergeRequest] | None:
    current_sprint: Sprint | None = Sprint.current_sprint()
    git_lab_group: Group | None = get_git_lab_group()
    if git_lab_group is None:
        return None
    return cast(
        typ=list[GroupMergeRequest],
        val=git_lab_group.mergerequests.list(
            get_all=True,
            updated_after=current_sprint.date_start.isoformat(),
            updated_before=current_sprint.date_end.isoformat(),
        )
    )
