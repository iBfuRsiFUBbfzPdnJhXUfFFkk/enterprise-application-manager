from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.models.service_provider import ServiceProvider
from core.views.generic.generic_500 import generic_500


def service_provider_delete_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        service_provider = ServiceProvider.objects.get(id=model_id)
        service_provider.delete()
    except ServiceProvider.DoesNotExist:
        return generic_500(request=request)

    return redirect('service_provider')
