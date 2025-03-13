from datetime import date

from django.db.models import QuerySet
from django.http import HttpRequest, JsonResponse, HttpResponse

from core.utilities.cast_query_set import cast_query_set
from git_lab.models.git_lab_issue import GitLabIssue
from git_lab.models.git_lab_iteration import GitLabIteration
from git_lab.models.git_lab_merge_request import GitLabMergeRequest
from git_lab.models.git_lab_user import GitLabUser
from kpi.models.key_performance_indicator_sprint import KeyPerformanceIndicatorSprint
from scrum.models.scrum_sprint import ScrumSprint


def kpi_sprints_api(
        request: HttpRequest,
) -> JsonResponse | HttpResponse:
    current_date = date.today()
    scrum_sprints: QuerySet[ScrumSprint] = cast_query_set(
        typ=ScrumSprint,
        val=ScrumSprint.objects.filter(date_end__lte=current_date)
    )
    git_lab_users: QuerySet[GitLabUser] = cast_query_set(
        typ=GitLabUser,
        val=GitLabUser.objects.all()
    )
    for scrum_sprint in scrum_sprints:
        for git_lab_user in git_lab_users:
            iterations: QuerySet[GitLabIteration] = scrum_sprint.iterations.all()
            kpi_sprint: KeyPerformanceIndicatorSprint = KeyPerformanceIndicatorSprint.objects.filter(
                git_lab_user=git_lab_user,
                scrum_sprint=scrum_sprint,
            ).first() or KeyPerformanceIndicatorSprint.objects.create(
                git_lab_user=git_lab_user,
                scrum_sprint=scrum_sprint,
            )
            issues_authored: QuerySet[GitLabIssue] = git_lab_user.issues_authored.filter(iteration__in=iterations)
            issues_assigned: QuerySet[GitLabIssue] = git_lab_user.issues_assigned.filter(iteration__in=iterations)
            issues_closed: QuerySet[GitLabIssue] = issues_assigned.filter(state="closed")
            merge_requests: QuerySet[GitLabMergeRequest] = git_lab_user.merge_requests_reviewed.filter(
                merged_at__date__gte=scrum_sprint.date_start,
                merged_at__date__lte=scrum_sprint.date_end,
            )
            kpi_sprint.name = f"{scrum_sprint.name} - {git_lab_user.username}"
            kpi_sprint.git_lab_iterations.add(*iterations)
            kpi_sprint.git_lab_issues.add(*issues_authored)
            kpi_sprint.number_of_merge_requests_approved = merge_requests.count()
            kpi_sprint.number_of_issues_written = issues_authored.count()
            kpi_sprint.number_of_story_points_committed_to = sum([
                issue.weight
                for issue
                in issues_assigned.all()
                if issue.weight is not None
            ])
            kpi_sprint.number_of_story_points_delivered = sum([
                issue.weight
                for issue
                in issues_closed.all()
                if issue.weight is not None and issue.closed_at.date() <= scrum_sprint.date_end
            ])
            kpi_sprint.save()
    return JsonResponse(data={}, safe=False)
