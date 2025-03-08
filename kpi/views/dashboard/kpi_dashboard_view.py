from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse

from core.models.sprint import Sprint
from core.utilities.base_render import base_render


def kpi_dashboard_view(request: HttpRequest) -> HttpResponse:
    last_five_sprints: QuerySet[Sprint] = Sprint.last_five_sprints()
    return base_render(
        context={
            "last_five_sprints": last_five_sprints,
        },
        request=request,
        template_name="authenticated/kpi/dashboard/kpi_dashboard.html"
    )
