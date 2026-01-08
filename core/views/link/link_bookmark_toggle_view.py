from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

from core.models.link import Link


@csrf_exempt
@login_required
@require_http_methods(["POST"])
def link_bookmark_toggle_view(request: HttpRequest, link_id: int) -> JsonResponse:
    """
    AJAX endpoint to toggle bookmark status for a link.
    Returns JSON with the new bookmark state.
    """
    try:
        link = Link.objects.get(id=link_id)
        user = request.user

        # Toggle bookmark
        if link.bookmarked_by.filter(id=user.id).exists():
            link.bookmarked_by.remove(user)
            is_bookmarked = False
        else:
            link.bookmarked_by.add(user)
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
