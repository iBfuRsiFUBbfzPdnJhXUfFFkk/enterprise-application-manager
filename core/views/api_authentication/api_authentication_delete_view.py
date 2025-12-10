from django.http import HttpRequest, HttpResponse
from core.models.api_authentication import APIAuthentication
from core.views.generic.generic_delete_view import generic_delete_view


def api_authentication_delete_view(
    request: HttpRequest, model_id: int
) -> HttpResponse:
    try:
        auth = APIAuthentication.objects.get(id=model_id)
        api_id = auth.api.id
    except APIAuthentication.DoesNotExist:
        api_id = None

    return generic_delete_view(
        model_cls=APIAuthentication,
        model_id=model_id,
        request=request,
        success_route='api_detail',
        success_route_kwargs={'model_id': api_id} if api_id else {},
    )
