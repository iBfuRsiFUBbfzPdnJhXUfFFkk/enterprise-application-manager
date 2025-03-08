from django.http import HttpRequest, JsonResponse, HttpResponse
from gitlab.v4.objects import GroupMember

from core.views.this_api.this_api_sync_git_lab_view.common.fetch.fetch_group_users import fetch_group_users


def git_lab_group_members_api(
        request: HttpRequest,
) -> JsonResponse:
    group_members: list[GroupMember] | None = fetch_group_users()
    print(group_members)
    return JsonResponse(data={})