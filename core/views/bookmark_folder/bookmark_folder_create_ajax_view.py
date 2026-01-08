import json

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from core.forms.bookmark_folder_form import BookmarkFolderForm


@csrf_exempt
@login_required
@require_http_methods(["POST"])
def bookmark_folder_create_ajax_view(request: HttpRequest) -> JsonResponse:
    """AJAX endpoint for creating a new bookmark folder."""
    try:
        data = json.loads(request.body)
        form = BookmarkFolderForm(user=request.user, data=data)

        if form.is_valid():
            folder = form.save()
            return JsonResponse({
                'success': True,
                'folder': {
                    'id': folder.id,
                    'name': folder.name,
                    'parent_folder_id': folder.parent_folder.id if folder.parent_folder else None,
                }
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'errors': {'_all': [str(e)]}
        }, status=500)
