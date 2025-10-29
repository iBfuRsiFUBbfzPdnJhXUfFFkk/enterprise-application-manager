from django.db import transaction
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.models.estimation_item import EstimationItem
from core.views.generic.generic_500 import generic_500


def estimation_item_move_down_view(request: HttpRequest, item_id: int) -> HttpResponse:
    """Move an estimation item down one position in the order."""
    try:
        item = EstimationItem.objects.get(id=item_id)
        estimation_id = item.estimation.id

        # Get the item immediately after this one in order
        next_item = EstimationItem.objects.filter(
            estimation=item.estimation,
            order__gt=item.order
        ).order_by('order').first()

        if next_item:
            # Swap the order values
            with transaction.atomic():
                item.order, next_item.order = next_item.order, item.order
                item.save(update_fields=['order'])
                next_item.save(update_fields=['order'])

    except EstimationItem.DoesNotExist:
        return generic_500(request=request)

    return redirect(to='estimation_detail', model_id=estimation_id)
