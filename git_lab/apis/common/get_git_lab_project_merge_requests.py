from datetime import datetime
from typing import cast

from dateutil.relativedelta import relativedelta
from django.db.models import QuerySet
from gitlab import GitlabListError, Gitlab, GitlabAuthenticationError
from gitlab.base import RESTObjectList
from gitlab.v4.objects import ProjectMergeRequest, Project

from core.settings.common.developer import DEBUG
from git_lab.apis.common.get_git_lab_projects import get_git_lab_projects
from git_lab.models.git_lab_project import GitLabProject


def get_git_lab_project_merge_requests(
        git_lab_client: Gitlab
) -> list[ProjectMergeRequest]:
    now: datetime = datetime.now()
    one_month_ago: datetime = now - relativedelta(months=1)
    git_lab_projects: QuerySet[GitLabProject] = get_git_lab_projects()
    all_project_merge_requests: set[ProjectMergeRequest] = set()
    for git_lab_project in git_lab_projects:
        try:
            project_id: int = git_lab_project.id
            project: Project | None = git_lab_client.projects.get(id=project_id, lazy=True)
            if project is None:
                continue
            project_merge_request_generator: RESTObjectList = project.mergerequests.list(
                    iterator=True,
                    state="all",
                    order_by="created_at",
                    sort="desc",
                    created_after=one_month_ago,
                )
            for project_merge_request in project_merge_request_generator:
                if DEBUG is True:
                    print(f"project_merge_request: {project_merge_request}")
                all_project_merge_requests.add(
                    cast(
                        typ=ProjectMergeRequest,
                        val=project_merge_request,
                    )
                )
        except GitlabListError as error:
            print(f"GitLabListError on {git_lab_project.name_with_namespace}: {error.error_message}")
            continue
        except GitlabAuthenticationError as error:
            print(f"GitlabAuthenticationError on {git_lab_project.name_with_namespace}: {error.error_message}")
            continue
    return list(all_project_merge_requests)
