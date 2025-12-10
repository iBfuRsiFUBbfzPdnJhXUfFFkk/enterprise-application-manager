from typing import Any, Mapping
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from core.forms.api_form import APIForm
from core.utilities.base_render import base_render


def api_add_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = APIForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='api')
    else:
        form = APIForm()

    context: Mapping[str, Any] = {'form': form}
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/api/api_form.html',
    )
