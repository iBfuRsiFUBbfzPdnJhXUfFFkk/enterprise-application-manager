from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from core.models.link import Link


@csrf_exempt
@login_required
@require_http_methods(["POST"])
def link_delete_ajax_view(request: HttpRequest, link_id: int) -> JsonResponse:
    """
    AJAX endpoint for deleting a link entirely.
    This will cascade delete all associated bookmarks.
    Returns JSON with success status or error message.
    """
    try:
        link = Link.objects.get(id=link_id)
        link_name = link.name
        link.delete()

        return JsonResponse({
            'success': True,
            'message': f'Link "{link_name}" has been deleted.'
        })

    except Link.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Link not found.'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
