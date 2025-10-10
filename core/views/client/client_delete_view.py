from django.http import HttpRequest, HttpResponse

from core.models.client import Client
from core.utilities.get_user_from_request import get_user_from_request
from core.utilities.wrap_with_global_context import wrap_with_global_context
from core.views.generic.generic_500 import generic_500


def client_delete_view(request: HttpRequest, model_id: int) -> HttpResponse:
    """
    Delete a client.
    """
    try:
        model = Client.objects.get(id=model_id)
        user = get_user_from_request(request)
        model._history_user = user
        model.delete()
    except Client.DoesNotExist:
        return generic_500(request, exception=Exception(f'Client with id {model_id} does not exist'))

    return wrap_with_global_context(
        context={'models': Client.objects.all()},
        request=request,
        template='authenticated/client/client.html',
    )
