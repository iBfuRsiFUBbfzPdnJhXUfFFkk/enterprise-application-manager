from typing import Mapping, Any

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.estimation_form import EstimationForm
from core.models.estimation import Estimation
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def estimation_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        estimation = Estimation.objects.get(id=model_id)
    except Estimation.DoesNotExist:
        return generic_500(request=request)

    if request.method == 'POST':
        form = EstimationForm(request.POST, instance=estimation)
        if form.is_valid():
            form.save()
            return redirect(to='estimation_detail', model_id=model_id)
    else:
        form = EstimationForm(instance=estimation)

    context: Mapping[str, Any] = {
        'form': form,
        'model': estimation
    }
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/estimation/estimation_form.html'
    )
