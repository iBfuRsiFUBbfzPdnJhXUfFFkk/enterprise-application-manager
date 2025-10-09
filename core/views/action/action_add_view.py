from typing import Mapping, Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.action_form import ActionForm
from core.utilities.base_render import base_render


def action_add_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = ActionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='action')
    else:
        form = ActionForm()

    context: Mapping[str, Any] = {'form': form}
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/action/action_form.html'
    )
