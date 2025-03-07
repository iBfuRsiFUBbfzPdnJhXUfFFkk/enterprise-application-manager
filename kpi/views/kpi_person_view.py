from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse

from core.models.person import Person
from core.models.sprint import Sprint
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500
from kpi.models.key_performance_indicator_sprint import KeyPerformanceIndicatorSprint
from kpi.utilities.calculate_average_metrics import AverageMetrics, calculate_average_metrics
from kpi.utilities.calculate_sprint_metrics import SprintMetrics, calculate_sprint_metrics


def kpi_person_view(request: HttpRequest, uuid: str) -> HttpResponse:
    person: Person | None = Person.from_uuid(uuid=uuid)
    if person is None:
        return generic_500(request=request)
    current_sprint: Sprint | None = Sprint.current_sprint()
    completed_sprints: QuerySet[Sprint] | None = Sprint.last_five()
    current_metrics: SprintMetrics | None = calculate_sprint_metrics(
        KeyPerformanceIndicatorSprint.objects.filter(
            sprint=current_sprint,
            person_developer=person,
        )
    ) if current_sprint else None
    completed_metrics: list[SprintMetrics | None] = [
        calculate_sprint_metrics(
            KeyPerformanceIndicatorSprint.objects.filter(
                sprint=sprint,
                person_developer=person,
            )
        )
        for sprint
        in completed_sprints
    ]
    avg_metrics: AverageMetrics | None = calculate_average_metrics(completed_metrics)

    kpi_sprints: QuerySet[KeyPerformanceIndicatorSprint] = KeyPerformanceIndicatorSprint.from_person(person=person)
    return base_render(
        context={
            "avg_metrics": avg_metrics,
            "current_metrics": current_metrics,
            "current_sprint": current_sprint,
            "kpi_sprints": kpi_sprints,
            "person": person,
        },
        request=request,
        template_name="authenticated/kpi/kpi_person.html"
    )
