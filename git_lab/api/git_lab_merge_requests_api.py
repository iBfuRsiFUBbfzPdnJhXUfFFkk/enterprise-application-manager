from typing import cast, TypedDict

from django.db.models import QuerySet
from django.http import HttpRequest, JsonResponse, HttpResponse
from gitlab import Gitlab
from gitlab.v4.objects import Group, GroupMergeRequest

from core.utilities.cast_query_set import cast_query_set
from core.utilities.git_lab.get_git_lab_client import get_git_lab_client
from core.views.generic.generic_500 import generic_500
from git_lab.models.git_lab_group import GitLabGroup

class GitLabMergeRequestUserTypedDict(TypedDict):
    avatar_url: str | None
    id: int | None
    locked: bool | None
    name: str | None
    state: str | None
    username: str | None
    web_url: str | None

class GitLabMergeRequestReferencesTypedDict(TypedDict):
    long: str | None
    relative: str | None
    short: str | None

class GitLabMergeRequestTimeStatsTypedDict(TypedDict):
    human_time_estimate: str | None
    human_total_time_spent: str | None
    time_estimate: int | None
    total_time_spent: int | None

class GitLabMergeRequestTaskCompletionStatusTypedDict(TypedDict):
    completed_count: int | None
    count: int | None

class GitLabMergeRequestTypedDict(TypedDict):
    assignee: GitLabMergeRequestUserTypedDict | None
    assignees: list[GitLabMergeRequestUserTypedDict] | None
    author: GitLabMergeRequestUserTypedDict | None
    blocking_discussions_resolved: bool | None
    closed_at: str | None
    created_at: str | None
    description: str | None
    draft: bool | None
    has_conflicts: bool | None
    id: int | None
    iid: int | None
    merged_at: str | None
    merged_by: GitLabMergeRequestUserTypedDict | None
    merged_user: GitLabMergeRequestUserTypedDict | None
    prepared_at: str | None
    project_id: int | None
    reference: str | None
    references: GitLabMergeRequestReferencesTypedDict | None
    reviewers: list[GitLabMergeRequestUserTypedDict] | None
    sha: str | None
    source_branch: str | None
    state: str | None
    target_branch: str | None
    task_completion_status: GitLabMergeRequestTaskCompletionStatusTypedDict | None
    time_stats: GitLabMergeRequestTimeStatsTypedDict | None
    title: str | None
    updated_at: str | None
    web_url: str | None


def git_lab_merge_requests_api(
        request: HttpRequest,
) -> JsonResponse | HttpResponse:
    git_lab_client: Gitlab | None = get_git_lab_client()
    if git_lab_client is None:
        return generic_500(request=request)
    git_lab_groups: QuerySet[GitLabGroup] = cast_query_set(
        typ=GitLabGroup,
        val=GitLabGroup.objects.all(),
    )
    all_merge_requests: set[GroupMergeRequest] = set()
    for git_lab_group in git_lab_groups:
        group: Group | None = git_lab_client.groups.get(id=git_lab_group.id)
        if group is None:
            continue
        merge_requests: list[GroupMergeRequest] = cast(
            typ=list[GroupMergeRequest],
            val=group.mergerequests.list(page=1, per_page=100)
        )
        for merge_request in merge_requests:
            all_merge_requests.add(merge_request)
    merge_request_dicts: list[GitLabMergeRequestTypedDict] = [project.asdict() for project in list(all_merge_requests)]
    return JsonResponse(data=merge_request_dicts, safe=False)
