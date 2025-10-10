from typing import Any, Mapping

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.hotfix_form import HotfixForm
from core.models.hotfix import Hotfix
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def hotfix_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        hotfix = Hotfix.objects.get(id=model_id)
    except Hotfix.DoesNotExist:
        return generic_500(request, exception=Exception(f'Hotfix with id {model_id} does not exist'))

    if request.method == 'POST':
        form = HotfixForm(request.POST, instance=hotfix)
        if form.is_valid():
            form.save()
            return redirect(to='hotfix')
    else:
        form = HotfixForm(instance=hotfix)

    context: Mapping[str, Any] = {'form': form}
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/hotfix/hotfix_form.html'
    )
