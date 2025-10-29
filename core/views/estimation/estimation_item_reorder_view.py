import json

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods

from core.models.estimation_item import EstimationItem


@login_required
@require_http_methods(["POST"])
def estimation_item_reorder_view(request: HttpRequest) -> JsonResponse:
    """
    Handle drag-and-drop reordering of estimation items.
    Expects a JSON payload with 'item_ids' as an array of item IDs in the new order.
    """
    try:
        data = json.loads(request.body)
        item_ids = data.get('item_ids', [])

        if not item_ids:
            return JsonResponse({'success': False, 'error': 'No item IDs provided'}, status=400)

        # Update order for each item
        with transaction.atomic():
            for index, item_id in enumerate(item_ids, start=1):
                EstimationItem.objects.filter(id=item_id).update(order=index)

        return JsonResponse({'success': True})

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
