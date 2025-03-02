from django.http import HttpResponse, HttpRequest

from core.utilities.base_render import base_render


def generic_500(request: HttpRequest | None = None) -> HttpResponse:
    return base_render(
        request=request,
        status=500,
        template_name='500.html',
    )
