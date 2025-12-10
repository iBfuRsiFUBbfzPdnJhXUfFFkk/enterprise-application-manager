from django.http import HttpRequest, HttpResponse
from core.models.api import API
from core.views.generic.generic_view import generic_view


def api_view(request: HttpRequest) -> HttpResponse:
    return generic_view(model_cls=API, name='api', request=request)
