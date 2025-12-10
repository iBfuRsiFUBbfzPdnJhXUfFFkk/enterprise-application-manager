from django.http import HttpRequest, HttpResponse
from core.models.api_request import APIRequest
from core.views.generic.generic_delete_view import generic_delete_view


def api_request_delete_view(
    request: HttpRequest, model_id: int
) -> HttpResponse:
    return generic_delete_view(
        model_cls=APIRequest,
        model_id=model_id,
        request=request,
        success_route='api_request',
    )
