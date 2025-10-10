from typing import Any, Mapping

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.data_use_exception_form import DataUseExceptionForm
from core.models.data_use_exception import DataUseException
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def data_use_exception_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        data_use_exception = DataUseException.objects.get(id=model_id)
    except DataUseException.DoesNotExist:
        return generic_500(request, exception=Exception(f'DataUseException with id {model_id} does not exist'))

    if request.method == 'POST':
        form = DataUseExceptionForm(request.POST, instance=data_use_exception)
        if form.is_valid():
            form.save()
            return redirect(to='data_use_exception')
    else:
        form = DataUseExceptionForm(instance=data_use_exception)

    context: Mapping[str, Any] = {'form': form}
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/data_use_exception/data_use_exception_form.html'
    )
