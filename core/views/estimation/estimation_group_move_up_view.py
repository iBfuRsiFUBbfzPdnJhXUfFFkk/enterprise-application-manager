from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from core.models.estimation import Estimation
from core.views.generic.generic_500 import generic_500


@csrf_exempt
@login_required
@require_http_methods(["POST"])
def estimation_group_move_up_view(request: HttpRequest, estimation_id: int) -> HttpResponse:
    """Move a group up one position in the order."""
    try:
        estimation = Estimation.objects.get(id=estimation_id)
        group_name = request.POST.get('group_name')

        if not group_name:
            return redirect(to='estimation_detail', model_id=estimation_id)

        # Get current group order or initialize if empty
        group_order = estimation.group_order if estimation.group_order else []

        # Get all unique groups from items
        all_groups = list(estimation.items.exclude(group__isnull=True).exclude(group='').values_list('group', flat=True).distinct())

        # Make sure group_order contains all groups
        for group in all_groups:
            if group not in group_order:
                group_order.append(group)

        # Find the index of the group
        if group_name in group_order:
            current_index = group_order.index(group_name)
            if current_index > 0:
                # Swap with the previous group
                group_order[current_index], group_order[current_index - 1] = group_order[current_index - 1], group_order[current_index]
                estimation.group_order = group_order
                estimation.save(update_fields=['group_order'])

        return redirect(to='estimation_detail', model_id=estimation_id)

    except Estimation.DoesNotExist:
        return generic_500(request=request)
