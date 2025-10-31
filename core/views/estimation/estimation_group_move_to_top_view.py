from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.models.estimation import Estimation
from core.views.generic.generic_500 import generic_500


def estimation_group_move_to_top_view(request: HttpRequest, estimation_id: int, group_name: str) -> HttpResponse:
    """Move a group to the top of the order."""
    try:
        estimation = Estimation.objects.get(id=estimation_id)

        # Get current group order or initialize if empty
        group_order = estimation.group_order if estimation.group_order else []

        # Get all unique groups from items
        all_groups = list(estimation.items.exclude(group__isnull=True).exclude(group='').values_list('group', flat=True).distinct())

        # Make sure group_order contains all groups
        for group in all_groups:
            if group not in group_order:
                group_order.append(group)

        # Remove the group from its current position and insert at the beginning
        if group_name in group_order:
            group_order.remove(group_name)
            group_order.insert(0, group_name)
            estimation.group_order = group_order
            estimation.save(update_fields=['group_order'])

        return redirect(to='estimation_detail', model_id=estimation_id)

    except Estimation.DoesNotExist:
        return generic_500(request=request)
