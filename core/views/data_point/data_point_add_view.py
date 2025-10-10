from typing import Mapping, Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.data_point_form import DataPointForm
from core.utilities.base_render import base_render


def data_point_add_view(request: HttpRequest) -> HttpResponse:
    """
    Create a new data point.
    """
    if request.method == 'POST':
        form = DataPointForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='data_point')
    else:
        form = DataPointForm()

    context: Mapping[str, Any] = {'form': form}
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/data_point/data_point_form.html'
    )
