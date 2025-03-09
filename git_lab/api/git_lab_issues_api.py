from typing import cast

from django.db.models import QuerySet
from django.http import HttpRequest, JsonResponse, HttpResponse
from gitlab import Gitlab
from gitlab.v4.objects import ProjectIssue, Project

from core.utilities.cast_query_set import cast_query_set
from core.utilities.convert_and_enforce_utc_timezone import convert_and_enforce_utc_timezone
from core.utilities.git_lab.get_git_lab_client import get_git_lab_client
from core.views.generic.generic_500 import generic_500
from git_lab.models.common.typed_dicts.git_lab_issue_typed_dict import GitLabIssueTypedDict
from git_lab.models.common.typed_dicts.git_lab_iteration_typed_dict import GitLabIterationTypedDict
from git_lab.models.common.typed_dicts.git_lab_links_typed_dict import GitLabLinksTypedDict
from git_lab.models.common.typed_dicts.git_lab_references_typed_dict import GitLabReferencesTypedDict
from git_lab.models.common.typed_dicts.git_lab_task_completion_status_typed_dict import \
    GitLabTaskCompletionStatusTypedDict
from git_lab.models.common.typed_dicts.git_lab_time_stats_typed_dict import GitLabTimeStatsTypedDict
from git_lab.models.common.typed_dicts.git_lab_user_reference_typed_dict import GitLabUserReferenceTypedDict
from git_lab.models.git_lab_issue import GitLabIssue
from git_lab.models.git_lab_iteration import GitLabIteration
from git_lab.models.git_lab_project import GitLabProject
from git_lab.models.git_lab_user import GitLabUser


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
            val=project.issues.list(all=True)
        )
        for issue in issues:
            all_issues.add(issue)
    issue_dicts: list[GitLabIssueTypedDict] = [issue.asdict() for issue in list(all_issues)]
    for issue_dict in issue_dicts:
        issue_id: int | None = issue_dict.get("id")
        if issue_id is None:
            continue
        git_lab_issue: GitLabIssue = GitLabIssue.objects.get_or_create(id=issue_id)[0]

        git_lab_issue.blocking_issues_count = issue_dict.get("blocking_issues_count")
        git_lab_issue.closed_at = convert_and_enforce_utc_timezone(
            datetime_string=issue_dict.get("closed_at"))
        git_lab_issue.created_at = convert_and_enforce_utc_timezone(
            datetime_string=issue_dict.get("created_at"))
        git_lab_issue.description = issue_dict.get("description")
        git_lab_issue.has_tasks = issue_dict.get("has_tasks")
        git_lab_issue.iid = issue_dict.get("iid")
        git_lab_issue.issue_type = issue_dict.get("issue_type")
        git_lab_issue.state = issue_dict.get("state")
        git_lab_issue.title = issue_dict.get("title")
        git_lab_issue.updated_at = convert_and_enforce_utc_timezone(
            datetime_string=issue_dict.get("updated_at"))
        git_lab_issue.user_notes_count = issue_dict.get("user_notes_count")
        git_lab_issue.web_url = issue_dict.get("web_url")
        git_lab_issue.weight = issue_dict.get("weight")
        references: GitLabReferencesTypedDict | None = issue_dict.get("references")
        if references is not None:
            git_lab_issue.references_long = references.get("full")
            git_lab_issue.references_relative = references.get("relative")
            git_lab_issue.references_short = references.get("short")
        task_completion_status: GitLabTaskCompletionStatusTypedDict | None = issue_dict.get(
            "task_completion_status")
        if task_completion_status is not None:
            git_lab_issue.task_completion_status_completed_count = task_completion_status.get("completed_count")
            git_lab_issue.task_completion_status_count = task_completion_status.get("count")
        time_stats: GitLabTimeStatsTypedDict | None = issue_dict.get("time_stats")
        if time_stats is not None:
            git_lab_issue.time_stats_human_time_estimate = time_stats.get("human_time_estimate")
            git_lab_issue.time_stats_human_total_time_spent = time_stats.get("human_total_time_spent")
            git_lab_issue.time_stats_time_estimate = time_stats.get("time_estimate")
            git_lab_issue.time_stats_total_time_spent = time_stats.get("total_time_spent")
        closed_by: GitLabUserReferenceTypedDict | None = issue_dict.get("closed_by")
        if closed_by is not None:
            git_lab_issue.closed_by = GitLabUser.objects.filter(id=closed_by.get("id")).first()
        author: GitLabUserReferenceTypedDict | None = issue_dict.get("author")
        if author is not None:
            git_lab_issue.author = GitLabUser.objects.filter(id=author.get("id")).first()
        git_lab_issue.project = GitLabProject.objects.filter(id=issue_dict.get("project_id")).first()
        assignees: list[GitLabUserReferenceTypedDict] | None = issue_dict.get("assignees")
        if assignees is not None:
            for assignee in assignees:
                user: GitLabUser | None = GitLabUser.objects.filter(id=assignee.get("id")).first()
                if user is not None:
                    git_lab_issue.assignees.add(user)
        links: GitLabLinksTypedDict | None = issue_dict.get("_links")
        if links is not None:
            git_lab_issue.link_award_emoji = links.get("award_emoji")
            git_lab_issue.link_notes = links.get("notes")
            git_lab_issue.link_project = links.get("project")
            git_lab_issue.link_self = links.get("self")
        iteration: GitLabIterationTypedDict | None = issue_dict.get("iteration")
        if iteration is not None:
            git_lab_issue.iteration = GitLabIteration.objects.filter(id=iteration.get("id")).first()
        git_lab_issue.save()
    return JsonResponse(data=issue_dicts, safe=False)
