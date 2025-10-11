from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.organization_form import OrganizationForm
from core.utilities.base_render import base_render


def organization_add_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = OrganizationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('organization')
    else:
        form = OrganizationForm()

    return base_render(
        request=request,
        template_name='authenticated/organization/organization_form.html',
        context={'form': form}
    )
