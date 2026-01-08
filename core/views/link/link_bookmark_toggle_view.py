import json

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from core.models.bookmark_folder import BookmarkFolder
from core.models.link import Link
from core.models.user_bookmark import UserBookmark


@csrf_exempt
@login_required
@require_http_methods(["POST"])
def link_bookmark_toggle_view(request: HttpRequest, link_id: int) -> JsonResponse:
    """
    AJAX endpoint to toggle bookmark status for a link.
    Optionally accepts folder_id to specify which folder to add bookmark to.
    Returns JSON with the new bookmark state.
    """
    try:
        link = Link.objects.get(id=link_id)
        user = request.user

        # Check if already bookmarked
        existing = UserBookmark.objects.filter(user=user, link=link).first()

        if existing:
            # Remove bookmark
            existing.delete()
            is_bookmarked = False
        else:
            # Add bookmark
            folder_id = None
            if request.body:
                try:
                    data = json.loads(request.body)
                    folder_id = data.get('folder_id')
                except json.JSONDecodeError:
                    pass

            folder = None
            if folder_id:
                folder = BookmarkFolder.objects.get(id=folder_id, user=user)

            UserBookmark.objects.create(
                user=user,
                link=link,
                folder=folder,
                order=0,
            )
            is_bookmarked = True

        return JsonResponse({
            'success': True,
            'is_bookmarked': is_bookmarked,
            'link_id': link.id,
        })

    except Link.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Link not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
