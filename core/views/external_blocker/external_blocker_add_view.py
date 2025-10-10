from typing import Any, Mapping

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.external_blocker_form import ExternalBlockerForm
from core.utilities.base_render import base_render


def external_blocker_add_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = ExternalBlockerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='external_blocker')
    else:
        form = ExternalBlockerForm()

    context: Mapping[str, Any] = {'form': form}
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/external_blocker/external_blocker_form.html'
    )
