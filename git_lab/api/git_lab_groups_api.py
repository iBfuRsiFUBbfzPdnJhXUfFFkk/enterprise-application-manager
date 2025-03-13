from typing import cast

from django.http import HttpRequest, JsonResponse, HttpResponse
from gitlab import Gitlab
from gitlab.v4.objects import Group, GroupSubgroup

from core.models.this_server_configuration import ThisServerConfiguration
from core.utilities.convert_and_enforce_utc_timezone import convert_and_enforce_utc_timezone
from core.utilities.git_lab.get_git_lab_client import get_git_lab_client
from core.views.generic.generic_500 import generic_500
from git_lab.api.common.get_common_query_parameters import GitLabApiCommonQueryParameters, get_common_query_parameters
from git_lab.models.common.typed_dicts.git_lab_group_typed_dict import GitLabGroupTypedDict
from git_lab.models.git_lab_group import GitLabGroup


def recurse_groups(
        all_groups: set[Group] | None = None,
        git_lab_client: Gitlab | None = None,
        parent_group: Group | None = None,
        query_parameters: GitLabApiCommonQueryParameters | None = None,
) -> set[Group]:
    if all_groups is None:
        all_groups = set()
    if git_lab_client is None:
        return all_groups
    if parent_group is None:
        return all_groups
    subgroups: list[GroupSubgroup] = cast(
        typ=list[GroupSubgroup],
        val=parent_group.subgroups.list(**(query_parameters or dict(all=True)))
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
            query_parameters=query_parameters,
        )
    return all_groups


def git_lab_groups_api(
        request: HttpRequest,
) -> JsonResponse | HttpResponse:
    query_parameters: GitLabApiCommonQueryParameters = get_common_query_parameters(request=request)
    git_lab_client: Gitlab | None = get_git_lab_client()
    if git_lab_client is None:
        return generic_500(request=request)
    connection_git_lab_top_level_group_id: str | None = ThisServerConfiguration.current().connection_git_lab_top_level_group_id
    if connection_git_lab_top_level_group_id is None:
        return generic_500(request=request)
    group_parent: Group | None = git_lab_client.groups.get(id=connection_git_lab_top_level_group_id)
    if group_parent is None:
        return generic_500(request=request)
    all_groups: set[Group] = recurse_groups(
        all_groups={group_parent},
        git_lab_client=git_lab_client,
        parent_group=group_parent,
        query_parameters=query_parameters,
    )
    group_dicts: list[GitLabGroupTypedDict] = [group.asdict() for group in list(all_groups)]
    for group_dict in group_dicts:
        group_id: int | None = group_dict.get("id")
        if group_id is None:
            continue
        get_or_create_tuple: tuple[GitLabGroup, bool] = GitLabGroup.objects.get_or_create(id=group_id)
        git_lab_group: GitLabGroup = get_or_create_tuple[0]
        git_lab_group.avatar_url = group_dict.get("avatar_url")
        git_lab_group.description = group_dict.get("description")
        git_lab_group.full_name = group_dict.get("full_name")
        git_lab_group.full_path = group_dict.get("full_path")
        git_lab_group.name = group_dict.get("name")
        git_lab_group.path = group_dict.get("path")
        git_lab_group.web_url = group_dict.get("web_url")
        git_lab_group.created_at = convert_and_enforce_utc_timezone(datetime_string=group_dict.get("created_at"))
        git_lab_group.save()
    return JsonResponse(data=group_dicts, safe=False)
