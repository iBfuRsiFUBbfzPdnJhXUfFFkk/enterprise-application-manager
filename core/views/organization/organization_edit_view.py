from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.organization_form import OrganizationForm
from core.models.organization import Organization
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def organization_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        organization = Organization.objects.get(id=model_id)
    except Organization.DoesNotExist:
        return generic_500(request=request)

    if request.method == 'POST':
        form = OrganizationForm(request.POST, instance=organization)
        if form.is_valid():
            form.save()
            return redirect('organization')
    else:
        form = OrganizationForm(instance=organization)

    return base_render(
        request=request,
        template_name='authenticated/organization/organization_form.html',
        context={'form': form}
    )
