from typing import Mapping, Any
from django.http import HttpRequest, HttpResponse

from core.models.estimation import Estimation
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def estimation_detail_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        estimation = Estimation.objects.get(id=model_id)
    except Estimation.DoesNotExist:
        return generic_500(request=request)

    # Get all items for this estimation
    items = estimation.items.all().order_by('id')

    # Get created and updated history records
    created_record = estimation.history.order_by('history_date').first()
    updated_record = estimation.history.order_by('-history_date').first()

    # Calculate totals
    totals = {
        'junior': estimation.get_total_hours_junior(),
        'mid': estimation.get_total_hours_mid(),
        'senior': estimation.get_total_hours_senior(),
        'lead': estimation.get_total_hours_lead(),
        'all_levels': estimation.get_total_hours_all_levels(),
        'contingency': estimation.get_contingency_hours(),
        'grand_total': estimation.get_grand_total_hours(),
    }

    context: Mapping[str, Any] = {
        'model': estimation,
        'items': items,
        'totals': totals,
        'created_record': created_record,
        'updated_record': updated_record,
    }
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/estimation/estimation_detail.html'
    )
