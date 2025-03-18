from datetime import datetime
from time import time

from dateutil.relativedelta import relativedelta
from django.db.models import QuerySet, Q
from django.http import HttpRequest, JsonResponse, HttpResponse
from gitlab import Gitlab

from core.utilities.cast_query_set import cast_query_set
from core.utilities.git_lab.get_git_lab_client import get_git_lab_client
from core.views.generic.generic_500 import generic_500
from git_lab.apis.git_lab_discussions_api.git_lab_discussions_api_payload import GitLabDiscussionsApiPayload, \
    initial_git_lab_discussions_api_payload
from git_lab.apis.git_lab_discussions_api.git_lab_discussions_api_process_project import \
    git_lab_discussions_api_process_project
from git_lab.models.git_lab_project import GitLabProject


def git_lab_discussions_api(
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
    model_projects: QuerySet[GitLabProject] = cast_query_set(
        typ=GitLabProject,
        val=GitLabProject.objects.filter(~Q(should_skip=True))
    )
    payload: GitLabDiscussionsApiPayload = initial_git_lab_discussions_api_payload
    for model_project in iter(model_projects.all()):
        payload: GitLabDiscussionsApiPayload = git_lab_discussions_api_process_project(
            created_after=created_after,
            git_lab_client=git_lab_client,
            model_project=model_project,
            payload=payload,
        )
    end_time: float = time()
    execution_time_in_seconds: float = end_time - start_time
    return JsonResponse(
        data={
            **payload,
            "execution_time_in_seconds": execution_time_in_seconds,
        },
        safe=False
    )
