import json
import logging

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from core.models.estimation_item import EstimationItem

logger = logging.getLogger(__name__)


@csrf_exempt
@login_required
@require_http_methods(["POST"])
def estimation_item_reorder_view(request: HttpRequest) -> JsonResponse:
    """
    Handle drag-and-drop reordering of estimation items.
    Expects a JSON payload with:
    - 'item_ids': array of item IDs in the new order
    - 'item_id' (optional): specific item being moved
    - 'new_group' (optional): new group name for the moved item (null for Ungrouped)
    """
    try:
        logger.info(f"Reorder request received. Body: {request.body}")
        data = json.loads(request.body)
        item_ids = data.get('item_ids', [])
        moved_item_id = data.get('item_id')
        new_group = data.get('new_group')

        if not item_ids:
            logger.warning("No item IDs provided in reorder request")
            return JsonResponse({'success': False, 'error': 'No item IDs provided'}, status=400)

        logger.info(f"Reordering items: {item_ids}, moved item: {moved_item_id}, new group: {new_group}")

        # Update order and optionally group for items
        with transaction.atomic():
            # If a specific item was moved to a new group, update its group
            if moved_item_id is not None and 'new_group' in data:
                EstimationItem.objects.filter(id=moved_item_id).update(group=new_group)
                logger.info(f"Updated item {moved_item_id} to group: {new_group}")

            # Update order for all items
            for index, item_id in enumerate(item_ids, start=1):
                EstimationItem.objects.filter(id=item_id).update(order=index)

        logger.info(f"Successfully reordered {len(item_ids)} items")
        return JsonResponse({'success': True})

    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        logger.error(f"Error reordering items: {e}", exc_info=True)
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
