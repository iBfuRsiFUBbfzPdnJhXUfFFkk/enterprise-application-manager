from django.db import transaction
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.models.estimation_item import EstimationItem
from core.views.generic.generic_500 import generic_500


def estimation_item_move_to_top_view(request: HttpRequest, item_id: int) -> HttpResponse:
    """Move an estimation item to the top (first position)."""
    try:
        item = EstimationItem.objects.get(id=item_id)
        estimation_id = item.estimation.id

        # Get all items for this estimation except the current one, ordered
        other_items = EstimationItem.objects.filter(
            estimation=item.estimation
        ).exclude(id=item_id).order_by('order', 'id')

        # Resequence: set this item to order 1, shift others down
        with transaction.atomic():
            item.order = 1
            item.save(update_fields=['order'])

            for index, other_item in enumerate(other_items, start=2):
                other_item.order = index
                other_item.save(update_fields=['order'])

    except EstimationItem.DoesNotExist:
        return generic_500(request=request)

    return redirect(to='estimation_detail', model_id=estimation_id)
