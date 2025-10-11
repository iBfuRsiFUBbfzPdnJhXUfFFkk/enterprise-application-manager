from django.http import HttpRequest, HttpResponse

from core.models.service_provider import ServiceProvider
from core.views.generic.generic_view import generic_view


def service_provider_view(request: HttpRequest) -> HttpResponse:
    return generic_view(
        model_cls=ServiceProvider,
        name='service_provider',
        request=request,
    )
