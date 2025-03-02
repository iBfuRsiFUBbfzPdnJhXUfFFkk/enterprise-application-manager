from django.http import HttpRequest, HttpResponse

from core.utilities.base_render import base_render


def home_view(request: HttpRequest) -> HttpResponse:
    return base_render(request=request, template_name="authenticated/home/home.html")
