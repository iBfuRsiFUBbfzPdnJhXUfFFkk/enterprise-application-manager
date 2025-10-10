from typing import Mapping, Any
from django.http import HttpRequest, HttpResponse

from core.models.client import Client
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def client_detail_view(request: HttpRequest, model_id: int) -> HttpResponse:
    """
    Display client details and change history.
    """
    try:
        client = Client.objects.get(id=model_id)
        historical_records = client.history.all()
    except Client.DoesNotExist:
        return generic_500(request, exception=Exception(f'Client with id {model_id} does not exist'))

    context: Mapping[str, Any] = {
        'client': client,
        'historical_records': historical_records,
    }
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/client/client_detail.html'
    )
