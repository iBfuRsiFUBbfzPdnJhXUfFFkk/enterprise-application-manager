from datetime import date
from time import time

from django.http import HttpRequest, HttpResponse
from gitlab.base import RESTObject

from core.models.person import Person
from core.models.sprint import Sprint
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500
from core.views.this_api.this_api_update_sprint_committed_issues_view.calculate_committed_issues import \
    calculate_committed_issues
from core.views.this_api.this_api_update_sprint_committed_issues_view.fetch_issues_by_iterations import \
    fetch_issues_by_iterations
from kpi.models.key_performance_indicator_sprint import KeyPerformanceIndicatorSprint


def this_api_update_sprint_committed_issues_view(request: HttpRequest) -> HttpResponse:
    start_time: float = time()
    current_date: date = date.today()
    try:
        sprints = Sprint.objects.filter(
            date_end__gte=current_date,
            date_start__lte=current_date,
        )
        if not sprints.exists():
            return generic_500(request=request)
    except Sprint.DoesNotExist:
        return generic_500(request=request)
    for sprint in sprints:
        all_group_issues: list[RESTObject] | None = fetch_issues_by_iterations(
            iteration_ids=[iteration.git_lab_id for iteration in sprint.git_lab_iteration_set.all()]
        )
        committed_issues = calculate_committed_issues(all_group_issues=all_group_issues)
        updated_count = 0
        for gitlab_username, data in committed_issues.items():
            total_weight = data["weight"]

            try:
                developer = Person.objects.get(gitlab_sync_username=gitlab_username)

                kpi, created = KeyPerformanceIndicatorSprint.objects.get_or_create(
                    person_developer=developer,
                    sprint=sprint,
                )
                kpi.number_of_story_points_committed_to = total_weight  # Update the committed field with total weight
                kpi.save()
                updated_count += 1
            except Person.DoesNotExist:
                continue

    end_time: float = time()
    execution_time_in_seconds: float = end_time - start_time
    return base_render(
        context={
            "execution_time_in_seconds": execution_time_in_seconds,
            "payload": {
            },
        },
        request=request,
        template_name="authenticated/action/action_success.html"
    )
