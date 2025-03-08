from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.urls import reverse

from core.models.person import Person
from core.models.sprint import Sprint
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500
from kpi.models.key_performance_indicator_sprint import KeyPerformanceIndicatorSprint
from kpi.utilities.scoped_metrics.calculate_scoped_metric import calculate_scoped_metric
from kpi.utilities.scoped_metrics.scoped_metric import ScopedMetric


def kpi_developer_view(request: HttpRequest, uuid: str) -> HttpResponse:
    developer: Person | None = Person.from_uuid(uuid=uuid)
    if developer is None:
        return generic_500(request=request)
    current_sprint: Sprint | None = Sprint.current_sprint()
    current_sprint_scoped_metric: ScopedMetric | None = calculate_scoped_metric(
        kpi_sprints=KeyPerformanceIndicatorSprint.from_person_current_sprint(person=developer)
    )
    last_five_sprints_scoped_metric: ScopedMetric | None = calculate_scoped_metric(
        kpi_sprints=KeyPerformanceIndicatorSprint.from_person_last_five_sprints(person=developer)
    )
    kpi_sprints: QuerySet[KeyPerformanceIndicatorSprint] = KeyPerformanceIndicatorSprint.from_person(person=developer)
    return base_render(
        context={
            "chart_url": reverse(viewname='kpi:kpi_chart_data_for_developer_ajax', kwargs={'uuid': developer.uuid}),
            "current_sprint": current_sprint,
            "current_sprint_scoped_metric": current_sprint_scoped_metric,
            "developer": developer,
            "kpi_sprints": kpi_sprints,
            "last_five_sprints_scoped_metric": last_five_sprints_scoped_metric,
        },
        request=request,
        template_name="authenticated/kpi/developer/kpi_developer.html"
    )
