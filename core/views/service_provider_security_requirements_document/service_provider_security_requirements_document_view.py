from django.http import HttpRequest, HttpResponse

from core.models.service_provider_security_requirements_document import ServiceProviderSecurityRequirementsDocument
from core.views.generic.generic_view import generic_view


def service_provider_security_requirements_document_view(request: HttpRequest) -> HttpResponse:
    return generic_view(
        model_cls=ServiceProviderSecurityRequirementsDocument,
        name='service_provider_security_requirements_document',
        request=request,
    )
