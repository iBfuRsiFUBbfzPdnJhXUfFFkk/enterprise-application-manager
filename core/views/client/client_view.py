from django.http import HttpRequest, HttpResponse

from core.models.client import Client
from core.views.generic.generic_view import generic_view


def client_view(request: HttpRequest) -> HttpResponse:
    """
    List all clients.
    """
    return generic_view(
        model_cls=Client,
        name='client',
        request=request,
    )
