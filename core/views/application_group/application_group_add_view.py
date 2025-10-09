from typing import Mapping, Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.application_group_form import ApplicationGroupForm
from core.utilities.base_render import base_render


def application_group_add_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = ApplicationGroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='application_group')
    else:
        form = ApplicationGroupForm()

    context: Mapping[str, Any] = {'form': form}
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/application_group/application_group_form.html'
    )
