import json

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from core.models.bookmark_folder import BookmarkFolder
from core.models.user_bookmark import UserBookmark


@csrf_exempt
@login_required
@require_http_methods(["POST"])
def bookmark_move_ajax_view(request: HttpRequest) -> JsonResponse:
    """
    AJAX endpoint to move a bookmark to a different folder and/or reorder it.
    Expects: {bookmark_id: int, folder_id: int|null, target_bookmark_id: int|null, position: 'before'|'after'}
    """
    try:
        data = json.loads(request.body)
        bookmark_id = data.get('bookmark_id')
        folder_id = data.get('folder_id')
        target_bookmark_id = data.get('target_bookmark_id')
        position = data.get('position', 'after')  # 'before' or 'after'

        bookmark = UserBookmark.objects.get(id=bookmark_id, user=request.user)

        # Update folder
        if folder_id:
            folder = BookmarkFolder.objects.get(id=folder_id, user=request.user)
            bookmark.folder = folder
        else:
            bookmark.folder = None  # Move to root

        # Update order based on target position
        if target_bookmark_id:
            target_bookmark = UserBookmark.objects.get(id=target_bookmark_id, user=request.user)

            # Get all bookmarks in the target folder, ordered
            siblings = UserBookmark.objects.filter(
                user=request.user,
                folder=bookmark.folder
            ).exclude(id=bookmark.id).order_by('order', 'id')

            # Reassign orders
            new_order = 0
            for sibling in siblings:
                if sibling.id == target_bookmark.id:
                    if position == 'before':
                        bookmark.order = new_order
                        new_order += 1
                        sibling.order = new_order
                    else:  # after
                        sibling.order = new_order
                        new_order += 1
                        bookmark.order = new_order
                else:
                    sibling.order = new_order

                new_order += 1
                sibling.save()
        else:
            # No target, append to end
            siblings = UserBookmark.objects.filter(
                user=request.user,
                folder=bookmark.folder
            ).exclude(id=bookmark.id)
            max_order = siblings.order_by('-order').first()
            bookmark.order = (max_order.order + 1) if max_order else 0

        bookmark.save()

        return JsonResponse({'success': True})
    except UserBookmark.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Bookmark not found'
        }, status=404)
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
