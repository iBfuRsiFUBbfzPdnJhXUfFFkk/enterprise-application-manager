from time import time

from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse

from kpi.models.key_performance_indicator_sprint import KeyPerformanceIndicatorSprint
from core.models.person import Person
from core.models.role import Role
from core.models.sprint import Sprint
from core.models.this_server_configuration import ThisServerConfiguration
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def this_api_create_sprint_kpis_view(request: HttpRequest) -> HttpResponse:
    start_time: float = time()
    this_server_configuration: ThisServerConfiguration | None = ThisServerConfiguration.objects.last()
    if this_server_configuration is None:
        return generic_500(request=request)
    scrum_capacity_base: int | None = this_server_configuration.scrum_capacity_base
    type_developer_role: Role | None = this_server_configuration.type_developer_role
    if type_developer_role is None:
        return generic_500(request=request)
    type_developer_role_id: int = type_developer_role.id
    sprints: QuerySet = Sprint.objects.all()
    if not sprints.exists():
        return generic_500(request=request)
    developers: QuerySet = Person.objects.filter(roles__in=[type_developer_role_id])
    if not developers.exists():
        return generic_500(request=request)
    number_of_created_records: int = 0
    for sprint in sprints:
        for developer in developers:
            if not KeyPerformanceIndicatorSprint.objects.filter(
                    person_developer=developer,
                    sprint=sprint,
            ).exists():
                KeyPerformanceIndicatorSprint.objects.create(
                    capacity_base=developer.scrum_capacity_base or scrum_capacity_base,
                    sprint=sprint,
                    person_developer=developer,
                )
                number_of_created_records += 1

    end_time: float = time()
    execution_time_in_seconds: float = end_time - start_time
    return base_render(
        context={
            "execution_time_in_seconds": execution_time_in_seconds,
            "payload": {
                "number_of_created_records": number_of_created_records,
            },
        },
        request=request,
        template_name="authenticated/action/action_success.html"
    )
