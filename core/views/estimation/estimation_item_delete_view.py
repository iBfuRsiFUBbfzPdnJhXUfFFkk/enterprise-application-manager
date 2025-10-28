from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.models.estimation_item import EstimationItem
from core.views.generic.generic_500 import generic_500


def estimation_item_delete_view(request: HttpRequest, item_id: int) -> HttpResponse:
    try:
        item = EstimationItem.objects.get(id=item_id)
        estimation_id = item.estimation.id
        item.delete()
    except EstimationItem.DoesNotExist:
        return generic_500(request=request)

    return redirect(to='estimation_detail', model_id=estimation_id)
