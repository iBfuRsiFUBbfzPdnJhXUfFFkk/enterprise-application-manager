from django.http import HttpRequest, HttpResponse

from core.models.sprint import Sprint
from core.utilities.base_render import base_render


def kpi_sprints_view(request: HttpRequest) -> HttpResponse:
    return base_render(
        context={
            "sprints": Sprint.objects.all(),
        },
        request=request,
        template_name="authenticated/kpi/sprint/kpi_sprints.html"
    )
