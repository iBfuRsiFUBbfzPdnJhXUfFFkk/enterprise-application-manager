from typing import cast, Any

from django.db.models import QuerySet
from django.http import HttpRequest, JsonResponse, HttpResponse
from gitlab import Gitlab
from gitlab.v4.objects import MergeRequest, ProjectMergeRequest

from core.utilities.cast_query_set import cast_query_set
from core.utilities.git_lab.get_git_lab_client import get_git_lab_client
from core.views.generic.generic_500 import generic_500
from git_lab.models.common.typed_dicts.git_lab_change_typed_dict import GitLabChangeTypedDict, \
    GitLabMergeRequestChangesTypedDict
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
        val=GitLabProject.objects.filter(id=284)
    )
    all_merge_request_changes: set[GitLabChangeTypedDict] = set()
    for git_lab_project in git_lab_projects:
        project_merge_requests: list[ProjectMergeRequest] | None = git_lab_client.projects.get(
            id=git_lab_project.id, lazy=True
        ).mergerequests.list(all=False, page=1, per_page=1, lazy=True)
        for project_merge_request in project_merge_requests:
            merge_request_change: GitLabMergeRequestChangesTypedDict = project_merge_request.changes()
            merge_request_changes: list[GitLabChangeTypedDict] | None = merge_request_change.get("changes")
            for change in merge_request_changes:
                diff: str | None = change.get("diff")
                if diff is None:
                    continue
                for line in diff.split("\n"):
                    print(line)
    # merge_request_dicts: list[GitLabMergeRequestTypedDict] = [project.asdict() for project in list(all_merge_request_changes)]
    for merge_request_change in list(all_merge_request_changes):
        continue
    print(all_merge_request_changes)
    return JsonResponse(data={}, safe=False)
