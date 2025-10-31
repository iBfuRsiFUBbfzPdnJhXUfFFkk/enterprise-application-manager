from typing import Mapping, Any

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.estimation_item_form import EstimationItemForm
from core.models.estimation_item import EstimationItem
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def estimation_item_edit_view(request: HttpRequest, item_id: int) -> HttpResponse:
    try:
        item = EstimationItem.objects.get(id=item_id)
    except EstimationItem.DoesNotExist:
        return generic_500(request=request)

    estimation = item.estimation

    if request.method == 'POST':
        form = EstimationItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect(to='estimation_detail', model_id=estimation.id)
    else:
        form = EstimationItemForm(instance=item)

    context: Mapping[str, Any] = {
        'form': form,
        'estimation': estimation,
        'item': item,
        'has_overridden_values': item.has_overridden_values()
    }
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/estimation/estimation_item_form.html'
    )
