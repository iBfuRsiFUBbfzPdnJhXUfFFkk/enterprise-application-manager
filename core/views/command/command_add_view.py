from typing import Mapping, Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.command_form import CommandForm
from core.utilities.base_render import base_render


def command_add_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = CommandForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='command')
    else:
        form = CommandForm()

    context: Mapping[str, Any] = {'form': form}
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/command/command_form.html'
    )
