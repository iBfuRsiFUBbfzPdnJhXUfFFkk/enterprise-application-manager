from django.http import HttpRequest, HttpResponse

from core.models.command import Command
from core.views.generic.generic_view import generic_view


def command_view(request: HttpRequest) -> HttpResponse:
    return generic_view(
        model_cls=Command,
        name='command',
        request=request,
    )
