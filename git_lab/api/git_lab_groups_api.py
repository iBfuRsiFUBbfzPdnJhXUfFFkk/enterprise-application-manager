from django.http import HttpRequest, JsonResponse, HttpResponse
from gitlab.v4.objects import GroupMember, Group

from core.views.this_api.this_api_sync_git_lab_view.common.fetch.fetch_git_lab_group import fetch_git_lab_group
from core.views.this_api.this_api_sync_git_lab_view.common.fetch.fetch_group_users import fetch_group_users


def get_groups(group):
    groups = []

    # Get child groups and get their members as well
    for subgroup in group.subgroups.list(all=True):
        groups.extend(get_groups(subgroup))

    return groups

def git_lab_groups_api(
        request: HttpRequest,
) -> JsonResponse:
    group_parent: Group | None = fetch_git_lab_group()
    print(get_groups(group_parent))
    return JsonResponse(data={})