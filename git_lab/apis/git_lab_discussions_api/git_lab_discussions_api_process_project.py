from datetime import datetime

from gitlab import Gitlab, GitlabListError, GitlabAuthenticationError
from gitlab.base import RESTObjectList
from gitlab.v4.objects import Project

from core.settings.common.developer import DEBUG
from git_lab.apis.git_lab_discussions_api.git_lab_discussions_api_payload import GitLabDiscussionsApiPayload, \
    initial_git_lab_discussions_api_payload
from git_lab.apis.git_lab_discussions_api.git_lab_discussions_api_process_merge_request import \
    git_lab_discussions_api_process_merge_request
from git_lab.models.git_lab_project import GitLabProject


def git_lab_discussions_api_process_project(
        created_after: datetime | None = None,
        git_lab_client: Gitlab | None = None,
        model_project: GitLabProject | None = None,
        payload: GitLabDiscussionsApiPayload | None = None,
) -> GitLabDiscussionsApiPayload:
    if payload is None:
        payload: GitLabDiscussionsApiPayload = initial_git_lab_discussions_api_payload
    if git_lab_client is None:
        return payload
    if model_project is None:
        return payload
    if DEBUG is True:
        print(f"Processing PROJECT: {model_project.web_url}")
    project_id: int = model_project.id
    rest_object_project: Project | None = git_lab_client.projects.get(id=project_id, lazy=False)
    if rest_object_project is None:
        return payload
    try:
        generator_merge_requests: RESTObjectList = rest_object_project.mergerequests.list(
            created_after=created_after,
            iterator=True,
            order_by="created_at",
            sort="desc",
            state="all",
        )
    except GitlabListError as error:
        print(f"GitLabListError on {model_project.name_with_namespace}: {error.error_message}")
        payload["total_number_of_projects_denied_access"] += 1
        return payload
    except GitlabAuthenticationError as error:
        print(f"GitlabAuthenticationError on {model_project.name_with_namespace}: {error.error_message}")
        payload["total_number_of_projects_denied_access"] += 1
        return payload
    for project_merge_request_rest_object in generator_merge_requests:
        payload: GitLabDiscussionsApiPayload = git_lab_discussions_api_process_merge_request(
            project_merge_request_rest_object=project_merge_request_rest_object,
            payload=payload,
        )
    return payload
