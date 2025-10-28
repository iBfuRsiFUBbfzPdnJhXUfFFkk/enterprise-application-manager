from typing import Mapping, Any

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.estimation_form import EstimationForm
from core.utilities.base_render import base_render


def estimation_add_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = EstimationForm(request.POST)
        if form.is_valid():
            estimation = form.save()
            return redirect(to='estimation_detail', model_id=estimation.id)
    else:
        form = EstimationForm()

    context: Mapping[str, Any] = {'form': form}
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/estimation/estimation_form.html'
    )
