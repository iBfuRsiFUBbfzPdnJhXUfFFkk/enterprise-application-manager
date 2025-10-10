from typing import Any, Mapping

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.data_use_exception_form import DataUseExceptionForm
from core.utilities.base_render import base_render


def data_use_exception_add_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = DataUseExceptionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='data_use_exception')
    else:
        form = DataUseExceptionForm()

    context: Mapping[str, Any] = {'form': form}
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/data_use_exception/data_use_exception_form.html'
    )
