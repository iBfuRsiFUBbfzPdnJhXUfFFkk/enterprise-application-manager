from django.db.models import Q
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse

from core.models.person import Person
from core.models.sprint import Sprint
from core.models.this_server_configuration import ThisServerConfiguration
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500
from kpi.models.key_performance_indicator_sprint import KeyPerformanceIndicatorSprint


def kpi_sprint_view(request: HttpRequest, uuid: str) -> HttpResponse:
    sprint: Sprint | None = Sprint.from_uuid(uuid=uuid)
    if sprint is None:
        return generic_500(request=request)
    developers_actively_employed: QuerySet[Person] = Person.developers_actively_employed()
    sprint_kpis: QuerySet[KeyPerformanceIndicatorSprint] = (
        KeyPerformanceIndicatorSprint
        .from_sprint(sprint=sprint)
        .filter(
            Q(person_developer__in=developers_actively_employed),
            ~Q(person_developer__in=ThisServerConfiguration.current().kpi_developers_to_exclude)
        )
    )

    return base_render(
        context={
            "sprint": sprint,
            "sprint_kpis": sprint_kpis,
        },
        request=request,
        template_name="authenticated/kpi/sprint/kpi_sprint.html"
    )
