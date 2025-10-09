from typing import Mapping, Any

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.application_form import ApplicationForm
from core.utilities.base_render import base_render


def application_add_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='application')
    else:
        form = ApplicationForm()

    context: Mapping[str, Any] = {'form': form}
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/application/application_form.html'
    )
