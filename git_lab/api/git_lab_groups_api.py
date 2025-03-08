from typing import cast

from django.http import HttpRequest, JsonResponse, HttpResponse
from gitlab import Gitlab
from gitlab.base import RESTObject
from gitlab.v4.objects import GroupMember, Group, GroupSubgroup

from core.models.this_server_configuration import ThisServerConfiguration
from core.utilities.git_lab.get_git_lab_client import get_git_lab_client
from core.views.this_api.this_api_sync_git_lab_view.common.fetch.fetch_git_lab_group import fetch_git_lab_group
from core.views.this_api.this_api_sync_git_lab_view.common.fetch.fetch_group_users import fetch_group_users


def recurse_groups(
        all_groups: set[Group],
        git_lab_client: Gitlab,
        parent_group: Group,
) -> set[Group]:
    subgroups: list[GroupSubgroup] = cast(
        typ=list[GroupSubgroup],
        val=parent_group.subgroups.list()
    )
    for subgroup in subgroups:
        child_group: Group | None = git_lab_client.groups.get(id=subgroup.id)
        if child_group is None:
            continue
        all_groups.add(child_group)
        all_groups = recurse_groups(
            all_groups=all_groups,
            git_lab_client=git_lab_client,
            parent_group=child_group,
        )
    return all_groups

def git_lab_groups_api(
        request: HttpRequest,
) -> JsonResponse:
    git_lab_client: Gitlab | None = get_git_lab_client()
    git_lab_group_id: str | None = ThisServerConfiguration.current().connection_git_lab_group_id
    group_parent =  git_lab_client.groups.get(id=git_lab_group_id, lazy=True)
    all_groups: set[Group] = recurse_groups(
        all_groups={group_parent},
        git_lab_client=group_parent.manager,
        parent_group=group_parent,
    )
    print(all_groups)
    print(len(all_groups))
    return JsonResponse(data={})