from django.http import HttpRequest, HttpResponse

from core.models.service_provider_security_requirements_document import ServiceProviderSecurityRequirementsDocument
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def service_provider_security_requirements_document_detail_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        service_provider_security_requirements_document = ServiceProviderSecurityRequirementsDocument.objects.get(id=model_id)
        historical_records = service_provider_security_requirements_document.history.all()
    except ServiceProviderSecurityRequirementsDocument.DoesNotExist:
        return generic_500(request=request)

    return base_render(
        request=request,
        template_name='authenticated/service_provider_security_requirements_document/service_provider_security_requirements_document_detail.html',
        context={
            'service_provider_security_requirements_document': service_provider_security_requirements_document,
            'historical_records': historical_records,
        }
    )
