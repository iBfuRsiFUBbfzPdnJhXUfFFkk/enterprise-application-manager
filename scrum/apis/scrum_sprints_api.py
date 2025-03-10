from django.db.models import QuerySet
from django.http import HttpRequest, JsonResponse, HttpResponse

from core.utilities.cast_query_set import cast_query_set
from git_lab.models.git_lab_iteration import GitLabIteration
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
            end_date=date_end,
            start_date=date_start,
        ).first() or ScrumSprint.objects.create()
        scrum_sprint.end_date = date_end
        scrum_sprint.start_date = date_start
        scrum_sprint.name = key
        scrum_sprint.save()
        for iteration in grouping_set:
            iteration.sprint = scrum_sprint
            iteration.save()
    return JsonResponse(data={}, safe=False)
