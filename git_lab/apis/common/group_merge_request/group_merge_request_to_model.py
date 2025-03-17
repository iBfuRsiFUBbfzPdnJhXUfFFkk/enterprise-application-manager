from core.utilities.convert_and_enforce_utc_timezone import convert_and_enforce_utc_timezone
from git_lab.models.common.typed_dicts.git_lab_merge_request_typed_dict import GitLabMergeRequestTypedDict
from git_lab.models.common.typed_dicts.git_lab_references_typed_dict import GitLabReferencesTypedDict
from git_lab.models.common.typed_dicts.git_lab_task_completion_status_typed_dict import \
    GitLabTaskCompletionStatusTypedDict
from git_lab.models.common.typed_dicts.git_lab_time_stats_typed_dict import GitLabTimeStatsTypedDict
from git_lab.models.common.typed_dicts.git_lab_user_reference_typed_dict import GitLabUserReferenceTypedDict
from git_lab.models.git_lab_merge_request import GitLabMergeRequest
from git_lab.models.git_lab_project import GitLabProject
from git_lab.models.git_lab_user import GitLabUser
from scrum.models.scrum_sprint import ScrumSprint


def group_merge_request_to_model(
        merge_request_dict: GitLabMergeRequestTypedDict,
) -> None:
    merge_request_id: int | None = merge_request_dict.get("id")
    if merge_request_id is None:
        return None
    get_or_create_tuple: tuple[GitLabMergeRequest, bool] = GitLabMergeRequest.objects.get_or_create(id=merge_request_id)
    git_lab_merge_request: GitLabMergeRequest = get_or_create_tuple[0]
    git_lab_merge_request.blocking_discussions_resolved = merge_request_dict.get("blocking_discussions_resolved")
    git_lab_merge_request.description = merge_request_dict.get("description")
    git_lab_merge_request.draft = merge_request_dict.get("draft") or False
    git_lab_merge_request.has_conflicts = merge_request_dict.get("has_conflicts") or False
    git_lab_merge_request.iid = merge_request_dict.get("iid")
    git_lab_merge_request.sha = merge_request_dict.get("sha")
    git_lab_merge_request.source_branch = merge_request_dict.get("source_branch")
    git_lab_merge_request.state = merge_request_dict.get("state")
    git_lab_merge_request.target_branch = merge_request_dict.get("target_branch")
    git_lab_merge_request.title = merge_request_dict.get("title")
    git_lab_merge_request.web_url = merge_request_dict.get("web_url")
    git_lab_merge_request.closed_at = convert_and_enforce_utc_timezone(
        datetime_string=merge_request_dict.get("closed_at")
    )
    git_lab_merge_request.created_at = convert_and_enforce_utc_timezone(
        datetime_string=merge_request_dict.get("created_at")
    )
    git_lab_merge_request.merged_at = convert_and_enforce_utc_timezone(
        datetime_string=merge_request_dict.get("merged_at")
    )
    git_lab_merge_request.prepared_at = convert_and_enforce_utc_timezone(
        datetime_string=merge_request_dict.get("prepared_at")
    )
    git_lab_merge_request.updated_at = convert_and_enforce_utc_timezone(
        datetime_string=merge_request_dict.get("updated_at")
    )
    references: GitLabReferencesTypedDict | None = merge_request_dict.get("references")
    if references is not None:
        git_lab_merge_request.references_long = references.get("long")
        git_lab_merge_request.references_relative = references.get("relative")
        git_lab_merge_request.references_short = references.get("short")
    task_completion_status: GitLabTaskCompletionStatusTypedDict | None = merge_request_dict.get(
        "task_completion_status"
    )
    if task_completion_status is not None:
        git_lab_merge_request.task_completion_status_completed_count = task_completion_status.get(
            "completed_count"
        ) or 0
        git_lab_merge_request.task_completion_status_count = task_completion_status.get("count") or 0
    time_stats: GitLabTimeStatsTypedDict | None = merge_request_dict.get("time_stats")
    if time_stats is not None:
        git_lab_merge_request.time_stats_human_time_estimate = time_stats.get("human_time_estimate")
        git_lab_merge_request.time_stats_human_total_time_spent = time_stats.get("human_total_time_spent")
        git_lab_merge_request.time_stats_time_estimate = time_stats.get("time_estimate")
        git_lab_merge_request.time_stats_total_time_spent = time_stats.get("total_time_spent")
    merged_by: GitLabUserReferenceTypedDict | None = merge_request_dict.get("merged_by")
    if merged_by is not None:
        git_lab_merge_request.merged_by = GitLabUser.objects.filter(id=merged_by.get("id")).first()
    closed_by: GitLabUserReferenceTypedDict | None = merge_request_dict.get("closed_by")
    if closed_by is not None:
        git_lab_merge_request.closed_by = GitLabUser.objects.filter(id=closed_by.get("id")).first()
    author: GitLabUserReferenceTypedDict | None = merge_request_dict.get("author")
    if author is not None:
        git_lab_merge_request.author = GitLabUser.objects.filter(id=author.get("id")).first()
    project: GitLabProject | None = GitLabProject.objects.filter(id=merge_request_dict.get("project_id")).first()
    if project is not None:
        git_lab_merge_request.project = project
        git_lab_merge_request.group = project.group
    reviewers: list[GitLabUserReferenceTypedDict] | None = merge_request_dict.get("reviewers")
    if reviewers is not None:
        for reviewer in reviewers:
            user: GitLabUser | None = GitLabUser.objects.filter(id=reviewer.get("id")).first()
            if user is not None:
                git_lab_merge_request.reviewers.add(user)
    assignees: list[GitLabUserReferenceTypedDict] | None = merge_request_dict.get("assignees")
    if assignees is not None:
        for assignee in assignees:
            user: GitLabUser | None = GitLabUser.objects.filter(id=assignee.get("id")).first()
            if user is not None:
                git_lab_merge_request.assignees.add(user)
    if git_lab_merge_request.merged_at is not None:
        scrum_sprint: ScrumSprint | None = ScrumSprint.objects.filter(
            date_start__lte=git_lab_merge_request.merged_at,
            date_end__gte=git_lab_merge_request.merged_at,
        ).first()
        if scrum_sprint is not None:
            git_lab_merge_request.scrum_sprint = scrum_sprint
    git_lab_merge_request.save()
