from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.db.models import QuerySet, Q
from django.http import HttpRequest, JsonResponse, HttpResponse
from gitlab import Gitlab

from core.utilities.cast_query_set import cast_query_set
from core.utilities.git_lab.get_git_lab_client import get_git_lab_client
from core.views.generic.generic_500 import generic_500
from git_lab.apis.git_lab_discussions_api.git_lab_discussions_api_payload import GitLabDiscussionsApiPayload, \
    initial_git_lab_discussions_api_payload, GitLabDiscussionsApiPayloadMergeRequest
from git_lab.apis.git_lab_discussions_api.git_lab_discussions_api_process_project import \
    git_lab_discussions_api_process_project
from git_lab.models.git_lab_project import GitLabProject

def filter_merge_requests(merge_requests: dict[int, GitLabDiscussionsApiPayloadMergeRequest]) -> dict[int, GitLabDiscussionsApiPayloadMergeRequest]:
    filtered = {}
    for mr_id, mr in merge_requests.items():
        discussions = mr.get("discussions")
        # Keep only merge requests that have a non-empty "discussions" dictionary.
        if discussions and isinstance(discussions, dict) and len(discussions) > 0:
            filtered[mr_id] = mr
    return filtered


def filter_projects(payload: GitLabDiscussionsApiPayload) -> GitLabDiscussionsApiPayload:
    projects = payload.get("projects")
    if not projects:
        return payload

    filtered_projects = {}
    for project_id, project in projects.items():
        merge_requests = project.get("merge_requests")
        if not merge_requests or not isinstance(merge_requests, dict):
            continue

        # Filter merge requests for the project.
        filtered_mrs = filter_merge_requests(merge_requests)
        # Only include the project if there is at least one merge request remaining.
        if filtered_mrs:
            project["merge_requests"] = filtered_mrs
            filtered_projects[project_id] = project

    payload["projects"] = filtered_projects
    return payload


# Example of combining with previous filtering (removing projects without any notes)
def process_payload(payload: GitLabDiscussionsApiPayload) -> GitLabDiscussionsApiPayload:
    # First, filter out projects without any notes
    projects = payload.get("projects")
    if projects:
        filtered_projects = {}
        for project_id, project in projects.items():
            merge_requests = project.get("merge_requests")
            if not merge_requests:
                continue

            project_has_notes = False
            for mr in merge_requests.values():
                discussions = mr.get("discussions")
                if not discussions:
                    continue
                for discussion in discussions.values():
                    notes = discussion.get("notes")
                    if notes and isinstance(notes, dict) and len(notes) > 0:
                        project_has_notes = True
                        break
                if project_has_notes:
                    break
            if project_has_notes:
                filtered_projects[project_id] = project

        payload["projects"] = filtered_projects
    payload = filter_projects(payload)
    return payload

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
        data=process_payload(payload),
        safe=False
    )
