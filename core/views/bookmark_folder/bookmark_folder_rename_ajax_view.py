import json

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from core.forms.bookmark_folder_form import BookmarkFolderForm
from core.models.bookmark_folder import BookmarkFolder


@csrf_exempt
@login_required
@require_http_methods(["POST"])
def bookmark_folder_rename_ajax_view(request: HttpRequest, folder_id: int) -> JsonResponse:
    """AJAX endpoint for renaming a bookmark folder."""
    try:
        data = json.loads(request.body)
        folder = BookmarkFolder.objects.get(id=folder_id, user=request.user)

        form = BookmarkFolderForm(user=request.user, data=data, instance=folder)
        if form.is_valid():
            folder = form.save()
            return JsonResponse({
                'success': True,
                'folder': {
                    'id': folder.id,
                    'name': folder.name,
                }
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            }, status=400)
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
