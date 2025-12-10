from django.http import HttpRequest, HttpResponse
from core.models.api_request import APIRequest
from core.views.generic.generic_view import generic_view


def api_request_view(request: HttpRequest) -> HttpResponse:
    return generic_view(
        model_cls=APIRequest, name='api_request', request=request
    )
