from re import search, Match

from django.db.models import QuerySet
from django.http import HttpRequest, JsonResponse, HttpResponse
from gitlab import Gitlab
from gitlab.v4.objects import ProjectMergeRequest

from core.utilities.cast_query_set import cast_query_set
from core.utilities.convert_and_enforce_utc_timezone import convert_and_enforce_utc_timezone
from core.utilities.git_lab.get_git_lab_client import get_git_lab_client
from core.views.generic.generic_500 import generic_500
from git_lab.models.common.typed_dicts.git_lab_change_typed_dict import GitLabChangeTypedDict, \
    GitLabMergeRequestChangesTypedDict, GitLabMergeRequestChangeDiffRefsTypedDict
from git_lab.models.common.typed_dicts.git_lab_references_typed_dict import GitLabReferencesTypedDict
from git_lab.models.common.typed_dicts.git_lab_task_completion_status_typed_dict import \
    GitLabTaskCompletionStatusTypedDict
from git_lab.models.common.typed_dicts.git_lab_time_stats_typed_dict import GitLabTimeStatsTypedDict
from git_lab.models.common.typed_dicts.git_lab_user_reference_typed_dict import GitLabUserReferenceTypedDict
from git_lab.models.git_lab_change import GitLabChange
from git_lab.models.git_lab_project import GitLabProject
from git_lab.models.git_lab_user import GitLabUser


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
        changes: list[GitLabChangeTypedDict] | None = change_dict.get("changes")
        total_lines_added: int = 0
        total_lines_removed: int = 0
        total_files_deleted: int = 0
        total_files_generated: int = 0
        total_files_created: int = 0
        total_files_renamed: int = 0
        for change in changes:
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
            if change.get("deleted_file") is True:
                total_files_deleted += 1
            if change.get("generated_file") is True:
                total_files_generated += 1
            if change.get("new_file") is True:
                total_files_created += 1
            if change.get("renamed_file") is True:
                total_files_renamed += 1
        git_lab_change: GitLabChange = GitLabChange.objects.get_or_create(id=change_dict.get("id"))[0]
        git_lab_change.created_at = convert_and_enforce_utc_timezone(datetime_string=change_dict.get("created_at"))
        git_lab_change.updated_at = convert_and_enforce_utc_timezone(datetime_string=change_dict.get("updated_at"))
        git_lab_change.latest_build_finished_at = convert_and_enforce_utc_timezone(
            datetime_string=change_dict.get("latest_build_finished_at"))
        git_lab_change.latest_build_started_at = convert_and_enforce_utc_timezone(
            datetime_string=change_dict.get("latest_build_started_at"))
        git_lab_change.merged_at = convert_and_enforce_utc_timezone(datetime_string=change_dict.get("merged_at"))
        git_lab_change.prepared_at = convert_and_enforce_utc_timezone(datetime_string=change_dict.get("prepared_at"))
        git_lab_change.description = change_dict.get("description")
        git_lab_change.title = change_dict.get("title")
        git_lab_change.iid = change_dict.get("iid")
        git_lab_change.web_url = change_dict.get("web_url")
        references: GitLabReferencesTypedDict | None = change_dict.get("references")
        task_completion_status: GitLabTaskCompletionStatusTypedDict | None = change_dict.get("task_completion_status")
        time_stats: GitLabTimeStatsTypedDict | None = change_dict.get("time_stats")
        if references is not None:
            git_lab_change.references_short = references.get("short")
            git_lab_change.references_long = references.get("full")
            git_lab_change.references_relative = references.get("relative")
        if task_completion_status is not None:
            git_lab_change.task_completion_status_completed_count = task_completion_status.get("completed_count")
            git_lab_change.task_completion_status_count = task_completion_status.get("count")
        if time_stats is not None:
            git_lab_change.time_stats_human_time_estimate = time_stats.get("human_time_estimate")
            git_lab_change.time_stats_human_total_time_spent = time_stats.get("human_total_time_spent")
            git_lab_change.time_stats_time_estimate = time_stats.get("time_estimate")
            git_lab_change.time_stats_total_time_spent = time_stats.get("total_time_spent")
        assignees: list[GitLabUserReferenceTypedDict] | None = change_dict.get("assignees")
        if assignees is not None:
            for assignee in assignees:
                user: GitLabUser | None = GitLabUser.objects.filter(id=assignee.get("id")).first()
                if user is not None:
                    git_lab_change.assignees.add(user)
        merged_by: GitLabUserReferenceTypedDict | None = change_dict.get("merged_by")
        if merged_by is not None:
            git_lab_change.merged_by = GitLabUser.objects.filter(id=merged_by.get("id")).first()
        closed_by: GitLabUserReferenceTypedDict | None = change_dict.get("closed_by")
        if closed_by is not None:
            git_lab_change.closed_by = GitLabUser.objects.filter(id=closed_by.get("id")).first()
        author: GitLabUserReferenceTypedDict | None = change_dict.get("author")
        if author is not None:
            git_lab_change.author = GitLabUser.objects.filter(id=author.get("id")).first()
        git_lab_change.project = GitLabProject.objects.filter(id=change_dict.get("project_id")).first()
        git_lab_change.changes_count = change_dict.get("changes_count")
        git_lab_change.draft = change_dict.get("draft")
        git_lab_change.has_conflicts = change_dict.get("has_conflicts")
        git_lab_change.merge_commit_sha = change_dict.get("merge_commit_sha")
        git_lab_change.sha = change_dict.get("sha")
        git_lab_change.squash_commit_sha = change_dict.get("squash_commit_sha")
        diff_refs: GitLabMergeRequestChangeDiffRefsTypedDict | None = change_dict.get("diff_refs")
        if diff_refs is not None:
            git_lab_change.head_sha = diff_refs.get("head_sha")
            git_lab_change.base_sha = diff_refs.get("base_sha")
            git_lab_change.start_sha = diff_refs.get("start_sha")
        git_lab_change.state = change_dict.get("state")
        git_lab_change.total_files_added = total_files_created
        git_lab_change.total_files_changed = len((changes or []))
        git_lab_change.total_files_deleted = total_files_deleted
        git_lab_change.total_files_generated = total_files_generated
        git_lab_change.total_files_renamed = total_files_renamed
        git_lab_change.total_lines_added = total_lines_added
        git_lab_change.total_lines_removed = total_lines_removed
        git_lab_change.save()
    return JsonResponse(data=change_dicts, safe=False)
