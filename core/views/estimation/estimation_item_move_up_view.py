from django.db import transaction
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.models.estimation_item import EstimationItem
from core.views.generic.generic_500 import generic_500


def estimation_item_move_up_view(request: HttpRequest, item_id: int) -> HttpResponse:
    """Move an estimation item up one position in the order."""
    try:
        item = EstimationItem.objects.get(id=item_id)
        estimation_id = item.estimation.id

        # Get the item immediately before this one in order
        previous_item = EstimationItem.objects.filter(
            estimation=item.estimation,
            order__lt=item.order
        ).order_by('-order').first()

        if previous_item:
            # Swap the order values
            with transaction.atomic():
                item.order, previous_item.order = previous_item.order, item.order
                item.save(update_fields=['order'])
                previous_item.save(update_fields=['order'])

    except EstimationItem.DoesNotExist:
        return generic_500(request=request)

    return redirect(to='estimation_detail', model_id=estimation_id)
