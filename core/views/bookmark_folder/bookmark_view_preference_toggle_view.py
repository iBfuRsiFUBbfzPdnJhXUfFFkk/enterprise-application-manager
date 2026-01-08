import json

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from core.models.common.enums.bookmark_view_preference_choices import (
    BOOKMARK_VIEW_CARD,
    BOOKMARK_VIEW_LIST,
)


@csrf_exempt
@login_required
@require_http_methods(["POST"])
def bookmark_view_preference_toggle_view(request: HttpRequest) -> JsonResponse:
    """Toggle between card and list view for bookmarks."""
    try:
        data = json.loads(request.body)
        view_mode = data.get('view_mode', BOOKMARK_VIEW_CARD)

        if view_mode not in [BOOKMARK_VIEW_CARD, BOOKMARK_VIEW_LIST]:
            return JsonResponse({
                'success': False,
                'error': 'Invalid view mode'
            }, status=400)

        request.user.bookmark_view_preference = view_mode
        request.user.save()

        return JsonResponse({
            'success': True,
            'view_mode': view_mode
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
