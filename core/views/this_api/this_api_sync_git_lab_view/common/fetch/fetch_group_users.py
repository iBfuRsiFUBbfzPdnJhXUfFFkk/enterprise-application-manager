from typing import cast

from gitlab import Gitlab
from gitlab.v4.objects import Group, GroupMember

from core.views.this_api.this_api_sync_git_lab_view.common.fetch.fetch_git_lab_group import fetch_git_lab_group


def fetch_group_users(
        git_lab_client: Gitlab | None = None,
        git_lab_group: Group | None = None,
) -> list[GroupMember] | None:
    if fetch_git_lab_group is None:
        git_lab_group: Group | None = fetch_git_lab_group(git_lab_client=git_lab_client)
    if git_lab_group is None:
        return None
    return cast(
        typ=list[GroupMember],
        val=git_lab_group.members.list(
            get_all=True,
            lazy=True,
        )
    )
