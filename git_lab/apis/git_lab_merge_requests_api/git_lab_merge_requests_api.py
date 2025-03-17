from typing import cast

from django.db.models import QuerySet
from django.http import HttpRequest, JsonResponse, HttpResponse
from gitlab import Gitlab, GitlabListError
from gitlab.v4.objects import Group, GroupMergeRequest

from core.utilities.cast_query_set import cast_query_set
from core.utilities.git_lab.get_git_lab_client import get_git_lab_client
from core.views.generic.generic_500 import generic_500
from git_lab.apis.common.get_common_query_parameters import GitLabApiCommonQueryParameters, get_common_query_parameters
from git_lab.apis.git_lab_merge_requests_api.git_lab_merge_requests_api_process_merge_request import \
    git_lab_merge_requests_api_process_merge_request
from git_lab.models.common.typed_dicts.git_lab_merge_request_typed_dict import GitLabMergeRequestTypedDict
from git_lab.models.git_lab_group import GitLabGroup


def git_lab_merge_requests_api(
        request: HttpRequest,
) -> JsonResponse | HttpResponse:
    query_parameters: GitLabApiCommonQueryParameters = get_common_query_parameters(request=request)
    git_lab_client: Gitlab | None = get_git_lab_client()
    if git_lab_client is None:
        return generic_500(request=request)
    git_lab_groups: QuerySet[GitLabGroup] = cast_query_set(
        typ=GitLabGroup,
        val=GitLabGroup.objects.all(),
    )
    all_merge_requests: set[GroupMergeRequest] = set()
    for git_lab_group in git_lab_groups:
        try:
            group: Group | None = git_lab_client.groups.get(id=git_lab_group.id)
            if group is None:
                continue
            merge_requests: list[GroupMergeRequest] = cast(
                typ=list[GroupMergeRequest],
                val=group.mergerequests.list(**query_parameters)
            )
        except GitlabListError as error:
            print(f"GitLabListError on {git_lab_group.full_path}: {error.error_message}")
            continue
        all_merge_requests.update(merge_requests)
    merge_request_dicts: list[GitLabMergeRequestTypedDict] = [
        merge_request.asdict()
        for merge_request
        in list(all_merge_requests)
    ]
    for merge_request_dict in merge_request_dicts:
        git_lab_merge_requests_api_process_merge_request(merge_request_dict=merge_request_dict)
    return JsonResponse(data=merge_request_dicts, safe=False)
