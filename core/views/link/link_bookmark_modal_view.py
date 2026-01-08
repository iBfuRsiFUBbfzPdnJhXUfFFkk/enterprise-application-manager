from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

from core.models.link import Link
from core.models.user_bookmark import UserBookmark


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

        # Get IDs of links already bookmarked by this user
        bookmarked_link_ids = UserBookmark.objects.filter(user=user).values_list('link_id', flat=True)

        # Get all links not bookmarked by this user
        unbookmarked_links = Link.objects.exclude(id__in=bookmarked_link_ids).values(
            'id', 'name', 'url', 'comment'
        )

        # Convert to list of dicts with proper null handling
        links_list = [
            {
                'id': link['id'],
                'name': link['name'],
                'url': link['url'],
                'comment': link['comment'] or ''
            }
            for link in unbookmarked_links
        ]

        return JsonResponse({
            'success': True,
            'links': links_list
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
