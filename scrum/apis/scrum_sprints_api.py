from datetime import datetime

from django.db.models import QuerySet
from django.http import HttpRequest, JsonResponse, HttpResponse

from core.utilities.cast_query_set import cast_query_set
from git_lab.models.git_lab_issue import GitLabIssue
from git_lab.models.git_lab_iteration import GitLabIteration
from git_lab.models.git_lab_merge_request import GitLabMergeRequest
from scrum.models.scrum_sprint import ScrumSprint


def get_iteration_key(iteration: GitLabIteration) -> str:
    return f"{iteration.start_date}=>{iteration.due_date}"


def scrum_sprints_api(
        request: HttpRequest,
) -> JsonResponse | HttpResponse:
    git_lab_iterations: QuerySet[GitLabIteration] = cast_query_set(
        typ=GitLabIteration,
        val=GitLabIteration.objects.all(),
    )
    iteration_groupings: dict[str, set[GitLabIteration]] = {}
    for git_lab_iteration in git_lab_iterations:
        key: str = get_iteration_key(iteration=git_lab_iteration)
        if key not in iteration_groupings:
            iteration_groupings[key] = set()
        iteration_groupings[key].add(git_lab_iteration)
    for key, grouping_set in iteration_groupings.items():
        date_start, date_end = key.split("=>")
        scrum_sprint: ScrumSprint = ScrumSprint.objects.filter(
            date_end=date_end,
            date_start=date_start,
        ).first() or ScrumSprint.objects.create()
        scrum_sprint.date_end = datetime.strptime(date_end, "%Y-%m-%d")
        scrum_sprint.date_start = datetime.strptime(date_start, "%Y-%m-%d")
        scrum_sprint.name = key
        scrum_sprint.save()
        total_issues: int = 0
        for iteration in grouping_set:
            iteration.sprint = scrum_sprint
            iteration.save()
            issues: QuerySet[GitLabIssue] = iteration.issues
            total_issues += issues.count()
        merge_requests: QuerySet[GitLabMergeRequest] = cast_query_set(
            typ=GitLabMergeRequest,
            val=GitLabMergeRequest.objects.filter(
                state="merged",
                merged_at__gte=scrum_sprint.date_start,
                merged_at__lte=scrum_sprint.date_end,
            )
        )
        for merge_request in merge_requests:
            merge_request.sprint = scrum_sprint
            merge_request.save()
        scrum_sprint.cached_total_number_of_issues = total_issues
        scrum_sprint.cached_total_number_of_merge_requests = merge_requests.count()
        scrum_sprint.save()
    return JsonResponse(data={}, safe=False)
