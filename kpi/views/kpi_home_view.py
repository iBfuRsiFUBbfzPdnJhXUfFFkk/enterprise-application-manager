from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse

from core.models.person import Person
from core.models.role import Role
from core.models.this_server_configuration import ThisServerConfiguration
from core.utilities.base_render import base_render
from core.utilities.this_server_configuration.get_current_server_configuration import get_current_server_configuration
from core.views.generic.generic_500 import generic_500


def kpi_home_view(request: HttpRequest) -> HttpResponse:
    this_server_configuration: ThisServerConfiguration | None = get_current_server_configuration()
    developer_role: Role | None = this_server_configuration.type_developer_role
    if developer_role is None:
        return generic_500(request=request)
    people: QuerySet = developer_role.people_who_hold_this_role
    return base_render(
        context={
            "people": people,
        },
        request=request,
        template_name="authenticated/kpi/kpi_home.html"
    )
