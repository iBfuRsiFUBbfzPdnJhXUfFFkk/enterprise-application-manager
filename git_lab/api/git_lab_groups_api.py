from typing import cast

from django.http import HttpRequest, JsonResponse
from gitlab import Gitlab
from gitlab.v4.objects import Group, GroupSubgroup

from core.models.this_server_configuration import ThisServerConfiguration
from core.utilities.git_lab.get_git_lab_client import get_git_lab_client
from git_lab.models.git_lab_group import GitLabGroup


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
    group_parent = git_lab_client.groups.get(id=git_lab_group_id, lazy=True)
    all_groups: set[Group] = recurse_groups(
        all_groups={group_parent},
        git_lab_client=git_lab_client,
        parent_group=group_parent,
    )
    group_dicts: list[dict] = [group.asdict() for group in list(all_groups)]
    for group_dict in group_dicts:
        GitLabGroup.objects.update_or_create(
            avatar_url=group_dict["avatar_url"],
            created_at=group_dict["created_at"],
            description=group_dict["description"],
            full_name=group_dict["full_name"],
            full_path=group_dict["full_path"],
            id=group_dict["id"],
            path=group_dict["path"],
            web_url=group_dict["web_url"],
        )
    return JsonResponse(data=group_dicts)
