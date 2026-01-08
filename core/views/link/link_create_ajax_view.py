import json

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from core.forms.link_form import LinkForm
from core.models.bookmark_folder import BookmarkFolder
from core.models.user_bookmark import UserBookmark


@csrf_exempt
@login_required
@require_http_methods(["POST"])
def link_create_ajax_view(request: HttpRequest) -> JsonResponse:
    """
    AJAX endpoint for creating a new link from a modal.
    Automatically bookmarks the link for the current user.
    Optionally accepts folder_id to specify which folder to add bookmark to.
    Returns JSON with the newly created link data or validation errors.
    """
    try:
        data = json.loads(request.body)
        folder_id = data.pop('folder_id', None)  # Extract folder_id

        form = LinkForm(data)

        if form.is_valid():
            link = form.save()

            # Create bookmark with optional folder
            folder = None
            if folder_id:
                folder = BookmarkFolder.objects.get(id=folder_id, user=request.user)

            UserBookmark.objects.create(
                user=request.user,
                link=link,
                folder=folder,
                order=0,
            )

            return JsonResponse({
                'success': True,
                'link': {
                    'id': link.id,
                    'name': link.name,
                    'url': link.url,
                    'comment': link.comment or ''
                }
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            }, status=400)

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'errors': {'_all': ['Invalid JSON data']}
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'errors': {'_all': [str(e)]}
        }, status=500)
