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

def remove_projects_without_notes(
    payload: GitLabDiscussionsApiPayload
) -> GitLabDiscussionsApiPayload:
    projects = payload.get("projects")
    if not projects:
        return payload

    filtered_projects = {}
    for project_id, project in projects.items():
        merge_requests = project.get("merge_requests")
        if not merge_requests:
            continue

        project_has_notes = False
        # Loop over merge requests
        for mr in merge_requests.values():
            discussions = mr.get("discussions")
            if not discussions:
                continue

            # Loop over discussions in the merge request
            for discussion in discussions.values():
                notes = discussion.get("notes")
                # Check if notes exists and has at least one entry
                if notes and isinstance(notes, dict) and len(notes) > 0:
                    project_has_notes = True
                    break
            if project_has_notes:
                break

        if project_has_notes:
            filtered_projects[project_id] = project

    payload["projects"] = filtered_projects
    return payload


def clean_empty_objects(obj):
    """
    Recursively remove keys in dictionaries whose values are empty dictionaries.
    For any dict, if a value is a dictionary, it will be processed recursively.
    If after cleaning, the dictionary is empty, it will be replaced with None.
    """
    if isinstance(obj, dict):
        # Create a new dict with cleaned values
        cleaned = {}
        for key, value in obj.items():
            new_value = clean_empty_objects(value)
            # Only keep the key if the cleaned value is not an empty dict
            # You may decide to also remove None values if that fits your needs.
            if new_value != {} and new_value is not None:
                cleaned[key] = new_value
        return cleaned
    elif isinstance(obj, list):
        # Process list items if necessary.
        return [clean_empty_objects(item) for item in obj if item != {}]
    else:
        return obj


def process_payload(payload: GitLabDiscussionsApiPayload) -> GitLabDiscussionsApiPayload:
    # First remove projects without any notes
    payload = remove_projects_without_notes(payload)
    # Then recursively clean empty dictionaries
    payload = clean_empty_objects(payload)
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
