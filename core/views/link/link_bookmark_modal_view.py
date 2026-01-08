from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

from core.models.link import Link


@csrf_exempt
@login_required
@require_http_methods(["GET"])
def link_bookmark_modal_view(request: HttpRequest) -> JsonResponse:
    """
    AJAX endpoint to get all links with their bookmark status for modal display.
    Returns JSON with links that are NOT currently bookmarked by the user.
    """
    try:
        user = request.user

        # Get all links not bookmarked by this user
        all_links = Link.objects.all().prefetch_related('bookmarked_by')
        unbookmarked_links = []

        for link in all_links:
            if not link.bookmarked_by.filter(id=user.id).exists():
                unbookmarked_links.append({
                    'id': link.id,
                    'name': link.name,
                    'url': link.url,
                    'comment': link.comment or ''
                })

        return JsonResponse({
            'success': True,
            'links': unbookmarked_links
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
