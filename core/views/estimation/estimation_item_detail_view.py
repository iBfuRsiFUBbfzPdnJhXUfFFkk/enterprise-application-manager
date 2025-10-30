from typing import Any, Mapping

from django.http import HttpRequest, HttpResponse

from core.models.estimation_item import EstimationItem
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def estimation_item_detail_view(request: HttpRequest, item_id: int) -> HttpResponse:
    """Display detailed view of an estimation item."""
    try:
        item = EstimationItem.objects.select_related('estimation').prefetch_related('links').get(id=item_id)
        estimation = item.estimation

        # Get created and updated history records
        created_record = item.history.order_by('history_date').first()
        updated_record = item.history.order_by('-history_date').first()

        context: Mapping[str, Any] = {
            'item': item,
            'estimation': estimation,
            'created_record': created_record,
            'updated_record': updated_record,
        }

        return base_render(
            context=context,
            request=request,
            template_name='authenticated/estimation/estimation_item_detail.html'
        )

    except EstimationItem.DoesNotExist:
        return generic_500(request=request)
