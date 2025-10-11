from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.service_provider_form import ServiceProviderForm
from core.models.service_provider import ServiceProvider
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def service_provider_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        service_provider = ServiceProvider.objects.get(id=model_id)
    except ServiceProvider.DoesNotExist:
        return generic_500(request=request)

    if request.method == 'POST':
        form = ServiceProviderForm(request.POST, instance=service_provider)
        if form.is_valid():
            form.save()
            return redirect('service_provider')
    else:
        form = ServiceProviderForm(instance=service_provider)

    return base_render(
        request=request,
        template_name='authenticated/service_provider/service_provider_form.html',
        context={'form': form}
    )
