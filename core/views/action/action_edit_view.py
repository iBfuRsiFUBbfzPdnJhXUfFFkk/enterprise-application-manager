from typing import Mapping, Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.action_form import ActionForm
from core.models.action import Action
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def action_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        action = Action.objects.get(id=model_id)
    except Action.DoesNotExist:
        return generic_500(request=request)

    if request.method == 'POST':
        form = ActionForm(request.POST, instance=action)
        if form.is_valid():
            form.save()
            return redirect(to='action')
    else:
        form = ActionForm(instance=action)

    context: Mapping[str, Any] = {'form': form}
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/action/action_form.html'
    )
