from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.service_provider_form import ServiceProviderForm
from core.utilities.base_render import base_render


def service_provider_add_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = ServiceProviderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('service_provider')
    else:
        form = ServiceProviderForm()

    return base_render(
        request=request,
        template_name='authenticated/service_provider/service_provider_form.html',
        context={'form': form}
    )
