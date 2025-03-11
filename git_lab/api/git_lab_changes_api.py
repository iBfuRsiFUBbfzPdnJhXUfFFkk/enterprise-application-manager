from typing import cast, Any

from django.db.models import QuerySet
from django.http import HttpRequest, JsonResponse, HttpResponse
from gitlab import Gitlab
from gitlab.v4.objects import MergeRequest

from core.utilities.cast_query_set import cast_query_set
from core.utilities.git_lab.get_git_lab_client import get_git_lab_client
from core.views.generic.generic_500 import generic_500
from git_lab.models.git_lab_merge_request import GitLabMergeRequest
from git_lab.models.git_lab_project import GitLabProject


def git_lab_changes_api(
        request: HttpRequest,
) -> JsonResponse | HttpResponse:
    fetch_per_group: int = request.GET.get('fetch_per_group', 25)
    git_lab_client: Gitlab | None = get_git_lab_client()
    if git_lab_client is None:
        return generic_500(request=request)
    git_lab_projects: QuerySet[GitLabProject] = cast_query_set(
        typ=GitLabProject,
        val=GitLabProject.objects.all()[::5],
    )
    all_merge_request_changes: set[dict[str, Any]] = set()
    for git_lab_project in git_lab_projects:
        changes: list[dict[str, Any]] | None = [x.changes for x in git_lab_client.projects.get(
            id=git_lab_project.id, lazy=True
        ).mergerequests.list(all=True, lazy=True)]
        if changes is None:
            continue
        for change in changes:
            all_merge_request_changes.add(change)
    # merge_request_dicts: list[GitLabMergeRequestTypedDict] = [project.asdict() for project in list(all_merge_request_changes)]
    for merge_request_change in list(all_merge_request_changes):
        continue
    return JsonResponse(data=list(all_merge_request_changes), safe=False)
