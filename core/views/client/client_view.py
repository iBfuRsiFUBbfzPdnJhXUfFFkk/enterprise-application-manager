from django.http import HttpRequest, HttpResponse

from core.models.client import Client
from core.utilities.wrap_with_global_context import wrap_with_global_context


def client_view(request: HttpRequest) -> HttpResponse:
    """
    List all clients.
    """
    return wrap_with_global_context(
        context={'models': Client.objects.all()},
        request=request,
        template='authenticated/client/client.html',
    )
