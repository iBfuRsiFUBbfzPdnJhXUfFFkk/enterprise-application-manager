from typing import Mapping, Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.command_form import CommandForm
from core.models.command import Command
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def command_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        command = Command.objects.get(id=model_id)
    except Command.DoesNotExist:
        return generic_500(request=request)

    if request.method == 'POST':
        form = CommandForm(request.POST, instance=command)
        if form.is_valid():
            form.save()
            return redirect(to='command')
    else:
        form = CommandForm(instance=command)

    context: Mapping[str, Any] = {'form': form}
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/command/command_form.html'
    )
