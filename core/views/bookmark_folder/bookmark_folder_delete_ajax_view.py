from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from core.models.bookmark_folder import BookmarkFolder


@csrf_exempt
@login_required
@require_http_methods(["POST"])
def bookmark_folder_delete_ajax_view(request: HttpRequest, folder_id: int) -> JsonResponse:
    """
    AJAX endpoint for deleting a bookmark folder.
    Moves all bookmarks to parent folder (or root if no parent).
    Moves all child folders to parent folder (or root if no parent).
    """
    try:
        folder = BookmarkFolder.objects.get(id=folder_id, user=request.user)
        parent = folder.parent_folder

        # Move bookmarks to parent
        folder.bookmarks.all().update(folder=parent)

        # Move child folders to parent
        folder.child_folders.all().update(parent_folder=parent)

        folder.delete()

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
