from datetime import datetime
from time import time

from dateutil.relativedelta import relativedelta
from django.db.models import QuerySet
from django.http import HttpRequest, JsonResponse, HttpResponse
from gitlab import Gitlab, GitlabListError, GitlabAuthenticationError
from gitlab.base import RESTObjectList
from gitlab.v4.objects import Group

from core.settings.common.developer import DEBUG
from core.utilities.cast_query_set import cast_query_set
from core.utilities.git_lab.get_git_lab_client import get_git_lab_client
from core.views.generic.generic_500 import generic_500
from git_lab.apis.git_lab_merge_requests_api.git_lab_merge_requests_api_process_merge_request import \
    git_lab_merge_requests_api_process_merge_request
from git_lab.models.common.typed_dicts.git_lab_merge_request_typed_dict import GitLabMergeRequestTypedDict
from git_lab.models.git_lab_group import GitLabGroup


def git_lab_merge_requests_api(
        request: HttpRequest,
) -> JsonResponse | HttpResponse:
    start_time: float = time()
    weeks_back_str: str = request.GET.get("weeks_back", "5")
    weeks_back: int = int(weeks_back_str)
    now: datetime = datetime.now()
    created_after: datetime = now - relativedelta(weeks=weeks_back)
    git_lab_client: Gitlab | None = get_git_lab_client()
    if git_lab_client is None:
        return generic_500(request=request)
    git_lab_groups: QuerySet[GitLabGroup] = cast_query_set(
        typ=GitLabGroup,
        val=GitLabGroup.objects.all(),
    )
    for git_lab_group in iter(git_lab_groups):
        if DEBUG is True:
            print(f"Processing GROUP: {git_lab_group.web_url}")
        try:
            group: Group | None = git_lab_client.groups.get(id=git_lab_group.id)
            if group is None:
                continue
            generator_merge_requests: RESTObjectList = group.mergerequests.list(
                created_after=created_after,
                iterator=True,
                order_by="created_at",
                sort="desc",
                state="all",
            )
        except GitlabListError as error:
            print(f"GitLabListError on {git_lab_group.full_path}: {error.error_message}")
            continue
        except GitlabAuthenticationError as error:
            print(f"GitLabAuthenticationError on {git_lab_group.full_path}: {error.error_message}")
            continue
        for merge_request in generator_merge_requests:
            merge_request_dict: GitLabMergeRequestTypedDict = merge_request.asdict()
            git_lab_merge_requests_api_process_merge_request(merge_request_dict=merge_request_dict)
    end_time: float = time()
    execution_time_in_seconds: float = end_time - start_time
    return JsonResponse(
        data={
            "execution_time_in_seconds": execution_time_in_seconds,
        },
        safe=False
    )
