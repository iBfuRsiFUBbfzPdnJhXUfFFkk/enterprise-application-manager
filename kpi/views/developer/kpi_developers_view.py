from django.http import HttpRequest, HttpResponse

from core.models.person import Person
from core.utilities.base_render import base_render


def kpi_developers_view(request: HttpRequest) -> HttpResponse:
    return base_render(
        context={
            "developers": Person.developers_actively_employed(),
        },
        request=request,
        template_name="authenticated/kpi/developer/kpi_developers.html"
    )
