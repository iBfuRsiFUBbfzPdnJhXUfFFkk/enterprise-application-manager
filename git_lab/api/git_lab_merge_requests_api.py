from typing import cast

from django.db.models import QuerySet
from django.http import HttpRequest, JsonResponse, HttpResponse
from gitlab import Gitlab
from gitlab.v4.objects import Group, GroupMergeRequest

from core.utilities.cast_query_set import cast_query_set
from core.utilities.convert_and_enforce_utc_timezone import convert_and_enforce_utc_timezone
from core.utilities.git_lab.get_git_lab_client import get_git_lab_client
from core.views.generic.generic_500 import generic_500
from git_lab.models.common.typed_dicts.git_lab_merge_request_typed_dict import GitLabMergeRequestTypedDict
from git_lab.models.common.typed_dicts.git_lab_references_typed_dict import GitLabReferencesTypedDict
from git_lab.models.common.typed_dicts.git_lab_task_completion_status_typed_dict import \
    GitLabTaskCompletionStatusTypedDict
from git_lab.models.common.typed_dicts.git_lab_time_stats_typed_dict import GitLabTimeStatsTypedDict
from git_lab.models.common.typed_dicts.git_lab_user_reference_typed_dict import GitLabUserReferenceTypedDict
from git_lab.models.git_lab_group import GitLabGroup
from git_lab.models.git_lab_merge_request import GitLabMergeRequest
from git_lab.models.git_lab_project import GitLabProject
from git_lab.models.git_lab_user import GitLabUser


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
    for merge_request_dict in merge_request_dicts:
        merge_request_id: int | None = merge_request_dict.get("id")
        if merge_request_id is None:
            continue
        git_lab_merge_request: GitLabMergeRequest = GitLabMergeRequest.objects.get_or_create(id=merge_request_id)[0]

        git_lab_merge_request.blocking_discussions_resolved = merge_request_dict.get("blocking_discussions_resolved")
        git_lab_merge_request.closed_at = convert_and_enforce_utc_timezone(
            datetime_string=merge_request_dict.get("closed_at"))
        git_lab_merge_request.created_at = convert_and_enforce_utc_timezone(
            datetime_string=merge_request_dict.get("created_at"))
        git_lab_merge_request.description = merge_request_dict.get("description")
        git_lab_merge_request.draft = merge_request_dict.get("draft")
        git_lab_merge_request.has_conflicts = merge_request_dict.get("has_conflicts")
        git_lab_merge_request.iid = merge_request_dict.get("iid")
        git_lab_merge_request.merged_at = convert_and_enforce_utc_timezone(
            datetime_string=merge_request_dict.get("merged_at"))
        git_lab_merge_request.prepared_at = convert_and_enforce_utc_timezone(
            datetime_string=merge_request_dict.get("prepared_at"))
        git_lab_merge_request.sha = merge_request_dict.get("sha")
        git_lab_merge_request.source_branch = merge_request_dict.get("source_branch")
        git_lab_merge_request.state = merge_request_dict.get("state")
        git_lab_merge_request.target_branch = merge_request_dict.get("target_branch")
        git_lab_merge_request.title = merge_request_dict.get("title")
        git_lab_merge_request.updated_at = convert_and_enforce_utc_timezone(
            datetime_string=merge_request_dict.get("updated_at"))
        git_lab_merge_request.web_url = merge_request_dict.get("web_url")
        references: GitLabReferencesTypedDict | None = merge_request_dict.get("references")
        if references is not None:
            git_lab_merge_request.references_long = references.get("long")
            git_lab_merge_request.references_relative = references.get("relative")
            git_lab_merge_request.references_short = references.get("short")
        task_completion_status: GitLabTaskCompletionStatusTypedDict | None = merge_request_dict.get(
            "task_completion_status")
        if task_completion_status is not None:
            git_lab_merge_request.task_completion_status_completed_count = task_completion_status.get("completed_count")
            git_lab_merge_request.task_completion_status_count = task_completion_status.get("count")
        time_stats: GitLabTimeStatsTypedDict | None = merge_request_dict.get("time_stats")
        if time_stats is not None:
            git_lab_merge_request.time_stats_human_time_estimate = time_stats.get("human_time_estimate")
            git_lab_merge_request.time_stats_human_total_time_spent = time_stats.get("human_total_time_spent")
            git_lab_merge_request.time_stats_time_estimate = time_stats.get("time_estimate")
            git_lab_merge_request.time_stats_total_time_spent = time_stats.get("total_time_spent")
        merged_by: GitLabUserReferenceTypedDict | None = merge_request_dict.get("merged_by")
        if merged_by is not None:
            git_lab_merge_request.merged_by = GitLabUser.objects.get(id=merged_by.get("id"))
        git_lab_merge_request.project = GitLabProject.objects.get(id=merge_request_dict.get("project_id"))
        reviewers: list[GitLabUserReferenceTypedDict] | None = merge_request_dict.get("reviewers")
        if reviewers is not None:
            for reviewer in reviewers:
                user: GitLabUser | None = GitLabUser.objects.get(id=reviewer.get("id"))
                if user is not None:
                    git_lab_merge_request.reviewers.add(user)
        git_lab_merge_request.save()
    return JsonResponse(data=merge_request_dicts, safe=False)
