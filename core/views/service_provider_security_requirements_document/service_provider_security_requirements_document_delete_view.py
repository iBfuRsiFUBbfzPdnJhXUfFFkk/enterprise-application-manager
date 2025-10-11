from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.models.service_provider_security_requirements_document import ServiceProviderSecurityRequirementsDocument
from core.views.generic.generic_500 import generic_500


def service_provider_security_requirements_document_delete_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        service_provider_security_requirements_document = ServiceProviderSecurityRequirementsDocument.objects.get(id=model_id)
        service_provider_security_requirements_document.delete()
    except ServiceProviderSecurityRequirementsDocument.DoesNotExist:
        return generic_500(request=request)

    return redirect('service_provider_security_requirements_document')
