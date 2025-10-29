from django.db import transaction
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.models.estimation import Estimation
from core.models.estimation_item import EstimationItem
from core.views.generic.generic_500 import generic_500


def estimation_fix_item_order_view(request: HttpRequest, model_id: int) -> HttpResponse:
    """
    Fix the ordering of estimation items by reassigning sequential order values.
    Orders items by their current order (NULL values last), then by ID.
    Useful when order values become corrupted or NULL.
    """
    try:
        estimation = Estimation.objects.get(id=model_id)

        # Get all items, ordering by current order (NULL values handled), then ID
        items = EstimationItem.objects.filter(estimation=estimation).order_by('order', 'id')

        # Reassign order values sequentially
        with transaction.atomic():
            for index, item in enumerate(items, start=1):
                item.order = index
                item.save(update_fields=['order'])

    except Estimation.DoesNotExist:
        return generic_500(request=request)

    return redirect(to='estimation_detail', model_id=model_id)
