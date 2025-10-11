from django.http import HttpRequest, HttpResponse

from core.models.server import Server
from core.views.generic.generic_view import generic_view


def server_view(request: HttpRequest) -> HttpResponse:
    return generic_view(
        model_cls=Server,
        name='server',
        request=request,
    )
