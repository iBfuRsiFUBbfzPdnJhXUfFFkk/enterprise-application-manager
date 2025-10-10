from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.models.client import Client
from core.views.generic.generic_500 import generic_500


def client_delete_view(request: HttpRequest, model_id: int) -> HttpResponse:
    """
    Delete a client.
    """
    try:
        client = Client.objects.get(id=model_id)
        client.delete()
    except Client.DoesNotExist:
        return generic_500(request=request)

    return redirect(to='client')
