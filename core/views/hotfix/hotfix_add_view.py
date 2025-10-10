from typing import Any, Mapping

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.hotfix_form import HotfixForm
from core.utilities.base_render import base_render


def hotfix_add_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = HotfixForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='hotfix')
    else:
        form = HotfixForm()

    context: Mapping[str, Any] = {'form': form}
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/hotfix/hotfix_form.html'
    )
