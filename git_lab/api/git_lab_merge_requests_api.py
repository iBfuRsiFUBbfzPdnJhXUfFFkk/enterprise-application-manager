from typing import cast

from django.db.models import QuerySet
from django.http import HttpRequest, JsonResponse, HttpResponse
from gitlab import Gitlab
from gitlab.v4.objects import Group, GroupMergeRequest

from core.utilities.cast_query_set import cast_query_set
from core.utilities.git_lab.get_git_lab_client import get_git_lab_client
from core.views.generic.generic_500 import generic_500
from git_lab.models.git_lab_group import GitLabGroup


def git_lab_merge_requests_api(
        request: HttpRequest,
) -> JsonResponse | HttpResponse:
    git_lab_client: Gitlab | None = get_git_lab_client()
    if git_lab_client is None:
        return generic_500(request=request)
    git_lab_groups: QuerySet[GitLabGroup] = cast_query_set(
        typ=GitLabGroup,
        val=GitLabGroup.objects.all(),
    )
    all_merge_requests: set[GroupMergeRequest] = set()
    for git_lab_group in git_lab_groups:
        group: Group | None = git_lab_client.groups.get(id=git_lab_group.id)
        if group is None:
            continue
        merge_requests: list[GroupMergeRequest] = cast(
            typ=list[GroupMergeRequest],
            val=group.mergerequests.list(page=1, per_page=100)
        )
        for merge_request in merge_requests:
            all_merge_requests.add(merge_request)
    merge_request_dicts: list[dict] = [project.asdict() for project in list(all_merge_requests)]
    return JsonResponse(data=merge_request_dicts, safe=False)
