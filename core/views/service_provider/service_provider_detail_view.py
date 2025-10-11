from django.http import HttpRequest, HttpResponse

from core.models.service_provider import ServiceProvider
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def service_provider_detail_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        service_provider = ServiceProvider.objects.get(id=model_id)
        historical_records = service_provider.history.all()
    except ServiceProvider.DoesNotExist:
        return generic_500(request=request)

    return base_render(
        request=request,
        template_name='authenticated/service_provider/service_provider_detail.html',
        context={
            'service_provider': service_provider,
            'historical_records': historical_records,
        }
    )
