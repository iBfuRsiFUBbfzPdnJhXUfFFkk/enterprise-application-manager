from typing import Mapping, Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.data_point_form import DataPointForm
from core.models.data_point import DataPoint
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def data_point_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    """
    Edit an existing data point.
    """
    try:
        model = DataPoint.objects.get(id=model_id)
    except DataPoint.DoesNotExist:
        return generic_500(request, exception=Exception(f'DataPoint with id {model_id} does not exist'))

    if request.method == 'POST':
        form = DataPointForm(request.POST, instance=model)
        if form.is_valid():
            form.save()
            return redirect(to='data_point')
    else:
        form = DataPointForm(instance=model)

    context: Mapping[str, Any] = {'form': form}
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/data_point/data_point_form.html'
    )
