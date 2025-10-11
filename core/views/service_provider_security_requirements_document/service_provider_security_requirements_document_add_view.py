from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.service_provider_security_requirements_document_form import ServiceProviderSecurityRequirementsDocumentForm
from core.utilities.base_render import base_render


def service_provider_security_requirements_document_add_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = ServiceProviderSecurityRequirementsDocumentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('service_provider_security_requirements_document')
    else:
        form = ServiceProviderSecurityRequirementsDocumentForm()

    return base_render(
        request=request,
        template_name='authenticated/service_provider_security_requirements_document/service_provider_security_requirements_document_form.html',
        context={'form': form}
    )
