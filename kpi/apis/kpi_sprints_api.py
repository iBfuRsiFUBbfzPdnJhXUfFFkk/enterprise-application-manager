from django.db.models import QuerySet
from django.http import HttpRequest, JsonResponse, HttpResponse

from core.utilities.cast_query_set import cast_query_set
from git_lab.models.git_lab_issue import GitLabIssue
from git_lab.models.git_lab_iteration import GitLabIteration
from git_lab.models.git_lab_user import GitLabUser
from kpi.models.key_performance_indicator_sprint import KeyPerformanceIndicatorSprint
from scrum.models.scrum_sprint import ScrumSprint


def kpi_sprints_api(
        request: HttpRequest,
) -> JsonResponse | HttpResponse:
    fetch_per_group: int = request.GET.get('fetch_per_group', 2)
    scrum_sprints: QuerySet[ScrumSprint] = cast_query_set(
        typ=ScrumSprint,
        val=ScrumSprint.objects.all()[::fetch_per_group]
    )
    git_lab_users: QuerySet[GitLabUser] = cast_query_set(
        typ=GitLabUser,
        val=GitLabUser.objects.all()
    )
    for scrum_sprint in scrum_sprints:
        for git_lab_user in git_lab_users:
            iterations: QuerySet[GitLabIteration] = scrum_sprint.iterations
            kpi_sprint: KeyPerformanceIndicatorSprint = KeyPerformanceIndicatorSprint.objects.filter(
                git_lab_user=git_lab_user,
                scrum_sprint=scrum_sprint,
            ).first() or KeyPerformanceIndicatorSprint.objects.create(
                git_lab_user=git_lab_user,
                scrum_sprint=scrum_sprint,
            )
            kpi_sprint.name = f"{scrum_sprint.name} - {git_lab_user.name}"
            issues: QuerySet[GitLabIssue] = git_lab_user.issues_authored.all().filter(iteration__in=iterations)
            kpi_sprint.number_of_issues_written = issues.count()
            kpi_sprint.save()
    return JsonResponse(data={}, safe=False)
