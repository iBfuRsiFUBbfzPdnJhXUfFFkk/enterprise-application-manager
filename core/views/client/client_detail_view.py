from django.http import HttpRequest, HttpResponse

from core.models.client import Client
from core.utilities.wrap_with_global_context import wrap_with_global_context
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

    return wrap_with_global_context(
        context={
            'client': client,
            'historical_records': historical_records,
        },
        request=request,
        template='authenticated/client/client_detail.html',
    )
