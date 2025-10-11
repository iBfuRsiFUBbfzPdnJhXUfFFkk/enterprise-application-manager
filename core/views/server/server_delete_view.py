from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.models.server import Server
from core.views.generic.generic_500 import generic_500


def server_delete_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        server = Server.objects.get(id=model_id)
        server.delete()
    except Server.DoesNotExist:
        return generic_500(request=request)

    return redirect('server')
