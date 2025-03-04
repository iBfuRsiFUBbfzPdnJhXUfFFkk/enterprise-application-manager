from django.http import HttpRequest, HttpResponse

from core.utilities.base_render import base_render


def kpi_home_view(request: HttpRequest) -> HttpResponse:
    return base_render(request=request, template_name="authenticated/kpi/kpi_home.html")
