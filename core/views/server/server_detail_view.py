from django.http import HttpRequest, HttpResponse

from core.models.server import Server
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def server_detail_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        server = Server.objects.get(id=model_id)
        historical_records = server.history.all()
    except Server.DoesNotExist:
        return generic_500(request=request)

    return base_render(
        request=request,
        template_name='authenticated/server/server_detail.html',
        context={
            'server': server,
            'historical_records': historical_records,
        }
    )
