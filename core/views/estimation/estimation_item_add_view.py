from typing import Mapping, Any

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.estimation_item_form import EstimationItemForm
from core.models.estimation import Estimation
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def estimation_item_add_view(request: HttpRequest, estimation_id: int) -> HttpResponse:
    try:
        estimation = Estimation.objects.get(id=estimation_id)
    except Estimation.DoesNotExist:
        return generic_500(request=request)

    if request.method == 'POST':
        form = EstimationItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.estimation = estimation
            item.save()
            return redirect(to='estimation_detail', model_id=estimation_id)
    else:
        form = EstimationItemForm(initial={'estimation': estimation})

    context: Mapping[str, Any] = {
        'form': form,
        'estimation': estimation
    }
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/estimation/estimation_item_form.html'
    )
