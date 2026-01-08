import json

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from core.models.bookmark_folder import BookmarkFolder


@csrf_exempt
@login_required
@require_http_methods(["POST"])
def bookmark_folder_reorder_ajax_view(request: HttpRequest) -> JsonResponse:
    """
    AJAX endpoint to move/reorder a folder.
    Expects: {folder_id: int, parent_folder_id: int|null, target_folder_id: int|null, position: 'before'|'after'}
    """
    try:
        data = json.loads(request.body)
        folder_id = data.get('folder_id')
        parent_folder_id = data.get('parent_folder_id')
        target_folder_id = data.get('target_folder_id')
        position = data.get('position', 'after')  # 'before' or 'after'

        folder = BookmarkFolder.objects.get(id=folder_id, user=request.user)

        # Check for circular reference
        if parent_folder_id:
            parent_folder = BookmarkFolder.objects.get(id=parent_folder_id, user=request.user)

            # Prevent folder from being its own parent
            if folder.id == parent_folder.id:
                return JsonResponse({
                    'success': False,
                    'error': 'A folder cannot be its own parent'
                }, status=400)

            # Prevent folder from being a descendant of itself
            current = parent_folder
            while current:
                if current.id == folder.id:
                    return JsonResponse({
                        'success': False,
                        'error': 'Cannot create circular folder structure'
                    }, status=400)
                current = current.parent_folder

            folder.parent_folder = parent_folder
        else:
            folder.parent_folder = None  # Move to root

        # Update order based on target position
        if target_folder_id:
            target_folder = BookmarkFolder.objects.get(id=target_folder_id, user=request.user)

            # Get all folders in the target parent, ordered
            siblings = BookmarkFolder.objects.filter(
                user=request.user,
                parent_folder=folder.parent_folder
            ).exclude(id=folder.id).order_by('order', 'id')

            # Reassign orders
            new_order = 0
            for sibling in siblings:
                if sibling.id == target_folder.id:
                    if position == 'before':
                        folder.order = new_order
                        new_order += 1
                        sibling.order = new_order
                    else:  # after
                        sibling.order = new_order
                        new_order += 1
                        folder.order = new_order
                else:
                    sibling.order = new_order

                new_order += 1
                sibling.save()
        else:
            # No target, append to end
            siblings = BookmarkFolder.objects.filter(
                user=request.user,
                parent_folder=folder.parent_folder
            ).exclude(id=folder.id)
            max_order_folder = siblings.order_by('-order').first()
            folder.order = (max_order_folder.order + 1) if max_order_folder else 0

        folder.save()

        return JsonResponse({'success': True})
    except BookmarkFolder.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Folder not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
