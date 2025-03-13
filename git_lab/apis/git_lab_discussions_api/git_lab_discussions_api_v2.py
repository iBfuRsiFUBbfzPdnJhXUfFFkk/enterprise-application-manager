from datetime import datetime

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


def git_lab_discussions_api_v2(
        request: HttpRequest,
) -> JsonResponse | HttpResponse:
    now: datetime = datetime.now()
    one_month_ago: datetime = now - relativedelta(months=1)
    git_lab_client: Gitlab | None = get_git_lab_client()
    if git_lab_client is None:
        return generic_500(request=request)
    model_projects: QuerySet[GitLabProject] = cast_query_set(
        typ=GitLabProject,
        val=GitLabProject.objects.filter(~Q(should_skip=True))
    )
    payload: GitLabDiscussionsApiPayload = initial_git_lab_discussions_api_payload
    for model_project in iter(model_projects.all()):
        payload["projects"][model_project.id] = {
            "merge_requests": {},
            "web_url": model_project.web_url,
        }
        payload: GitLabDiscussionsApiPayload = git_lab_discussions_api_process_project(
            created_after=one_month_ago,
            git_lab_client=git_lab_client,
            model_project=model_project,
            payload=payload,
        )
    return JsonResponse(
        data=payload,
        safe=False
    )
