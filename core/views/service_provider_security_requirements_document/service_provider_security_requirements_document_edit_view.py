from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.service_provider_security_requirements_document_form import ServiceProviderSecurityRequirementsDocumentForm
from core.models.service_provider_security_requirements_document import ServiceProviderSecurityRequirementsDocument
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def service_provider_security_requirements_document_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        service_provider_security_requirements_document = ServiceProviderSecurityRequirementsDocument.objects.get(id=model_id)
    except ServiceProviderSecurityRequirementsDocument.DoesNotExist:
        return generic_500(request=request)

    if request.method == 'POST':
        form = ServiceProviderSecurityRequirementsDocumentForm(request.POST, instance=service_provider_security_requirements_document)
        if form.is_valid():
            form.save()
            return redirect('service_provider_security_requirements_document')
    else:
        form = ServiceProviderSecurityRequirementsDocumentForm(instance=service_provider_security_requirements_document)

    return base_render(
        request=request,
        template_name='authenticated/service_provider_security_requirements_document/service_provider_security_requirements_document_form.html',
        context={'form': form}
    )
