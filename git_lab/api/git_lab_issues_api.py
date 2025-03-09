from typing import cast

from django.db.models import QuerySet
from django.http import HttpRequest, JsonResponse, HttpResponse
from gitlab import Gitlab
from gitlab.v4.objects import ProjectIssue, Project

from core.utilities.cast_query_set import cast_query_set
from core.utilities.git_lab.get_git_lab_client import get_git_lab_client
from core.views.generic.generic_500 import generic_500
from git_lab.models.git_lab_project import GitLabProject


def git_lab_issues_api(
        request: HttpRequest,
) -> JsonResponse | HttpResponse:
    git_lab_client: Gitlab | None = get_git_lab_client()
    if git_lab_client is None:
        return generic_500(request=request)
    git_lab_projects: QuerySet[GitLabProject] = cast_query_set(
        typ=GitLabProject,
        val=GitLabProject.objects.all(),
    )
    all_issues: set[ProjectIssue] = set()
    for git_lab_project in git_lab_projects:
        project: Project | None = git_lab_client.projects.get(id=git_lab_project.id)
        if project is None:
            continue
        issues: list[ProjectIssue] = cast(
            typ=list[ProjectIssue],
            val=project.issues.list(page=1, per_page=100)
        )
        for issue in issues:
            all_issues.add(issue)
    issue_dicts: list[dict] = [issue.asdict() for issue in list(all_issues)]
    return JsonResponse(data=issue_dicts, safe=False)
