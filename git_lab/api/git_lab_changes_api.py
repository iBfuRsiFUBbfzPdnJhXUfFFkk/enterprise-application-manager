from re import search, Match

from django.db.models import QuerySet
from django.http import HttpRequest, JsonResponse, HttpResponse
from gitlab import Gitlab
from gitlab.v4.objects import ProjectMergeRequest

from core.utilities.cast_query_set import cast_query_set
from core.utilities.git_lab.get_git_lab_client import get_git_lab_client
from core.views.generic.generic_500 import generic_500
from git_lab.models.common.typed_dicts.git_lab_change_typed_dict import GitLabChangeTypedDict, \
    GitLabMergeRequestChangesTypedDict
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
    all_project_merge_requests: set[ProjectMergeRequest] = set()
    for git_lab_project in git_lab_projects:
        project_merge_requests: list[ProjectMergeRequest] | None = git_lab_client.projects.get(
            id=git_lab_project.id, lazy=True
        ).mergerequests.list(all=False, page=1, per_page=1, lazy=True)
        if project_merge_requests is None:
            continue
        all_project_merge_requests.add(*project_merge_requests)

    change_dicts: list[GitLabMergeRequestChangesTypedDict] = [
        project_merge_request.changes()
        for project_merge_request
        in list(all_project_merge_requests)
    ]
    for change_dict in change_dicts:
        merge_request_changes: list[GitLabChangeTypedDict] | None = change_dict.get("changes")
        total_lines_added: int = 0
        total_lines_removed: int = 0
        for change in merge_request_changes:
            diff: str | None = change.get("diff")
            if diff is None or len(diff.strip()) == 0:
                continue
            match: Match[str] | None = search(pattern=r'@@ -\d+,\d+ \+\d+,\d+ @@', string=diff)
            if match is None:
                continue
            group: str = match.group(0)
            round_one_split: list[str] = group.split(" ")
            removed_split: str = round_one_split[1]
            added_split: str = round_one_split[2]
            lines_removed: str = removed_split.split(",")[1]
            lines_added: str = added_split.split(",")[1]
            total_lines_removed += int(lines_removed)
            total_lines_added += int(lines_added)
        print(f"total_lines_added: {total_lines_added}")
        print(f"total_lines_removed: {total_lines_removed}")
    return JsonResponse(data=change_dicts, safe=False)
