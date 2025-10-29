from typing import Mapping, Any
from collections import OrderedDict
from decimal import Decimal
from django.http import HttpRequest, HttpResponse

from core.models.estimation import Estimation
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def estimation_detail_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        estimation = Estimation.objects.get(id=model_id)
    except Estimation.DoesNotExist:
        return generic_500(request=request)

    # Get all items for this estimation, ordered by the order field
    items = estimation.items.all().order_by('order', 'id')

    # Group items by their group field with subtotals
    grouped_items = OrderedDict()
    # Put ungrouped items first (None or empty string)
    grouped_items['Ungrouped'] = {'items': [], 'subtotals': {}}

    for item in items:
        group_name = item.group if item.group else 'Ungrouped'
        if group_name not in grouped_items:
            grouped_items[group_name] = {'items': [], 'subtotals': {}}
        grouped_items[group_name]['items'].append(item)

    # Remove Ungrouped if it's empty
    if not grouped_items['Ungrouped']['items']:
        del grouped_items['Ungrouped']

    # Calculate subtotals for each group
    for group_name, group_data in grouped_items.items():
        group_items_list = group_data['items']
        subtotals = {
            'story_points': sum(item.story_points or Decimal('0') for item in group_items_list),
            'junior_with_uncertainty': sum(item.get_junior_hours_with_uncertainty() for item in group_items_list),
            'mid_with_uncertainty': sum(item.get_mid_hours_with_uncertainty() for item in group_items_list),
            'senior_with_uncertainty': sum(item.get_senior_hours_with_uncertainty() for item in group_items_list),
            'lead_with_uncertainty': sum(item.get_lead_hours_with_uncertainty() for item in group_items_list),
            'reviewer_hours': sum(item.get_reviewer_hours() for item in group_items_list),
        }
        group_data['subtotals'] = subtotals

    # Get created and updated history records
    created_record = estimation.history.order_by('history_date').first()
    updated_record = estimation.history.order_by('-history_date').first()

    # Calculate totals per level (with uncertainty and contingency)
    totals = {
        'base_junior': estimation.get_base_hours_junior(),
        'base_mid': estimation.get_base_hours_mid(),
        'base_senior': estimation.get_base_hours_senior(),
        'base_lead': estimation.get_base_hours_lead(),
        'junior_with_uncertainty': estimation.get_total_hours_junior_with_uncertainty(),
        'mid_with_uncertainty': estimation.get_total_hours_mid_with_uncertainty(),
        'senior_with_uncertainty': estimation.get_total_hours_senior_with_uncertainty(),
        'lead_with_uncertainty': estimation.get_total_hours_lead_with_uncertainty(),
        'contingency_junior': estimation.get_contingency_hours_junior(),
        'contingency_mid': estimation.get_contingency_hours_mid(),
        'contingency_senior': estimation.get_contingency_hours_senior(),
        'contingency_lead': estimation.get_contingency_hours_lead(),
        'grand_total_junior': estimation.get_grand_total_hours_junior(),
        'grand_total_mid': estimation.get_grand_total_hours_mid(),
        'grand_total_senior': estimation.get_grand_total_hours_senior(),
        'grand_total_lead': estimation.get_grand_total_hours_lead(),
        'average_with_uncertainty': estimation.get_average_hours_with_uncertainty(),
        'total_story_points': estimation.get_total_story_points(),
    }

    context: Mapping[str, Any] = {
        'model': estimation,
        'items': items,
        'grouped_items': grouped_items,
        'totals': totals,
        'created_record': created_record,
        'updated_record': updated_record,
    }
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/estimation/estimation_detail.html'
    )
