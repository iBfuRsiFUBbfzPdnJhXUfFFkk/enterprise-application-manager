import json

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST

from core.models.application_pin import ApplicationPin
from core.utilities.get_user_from_request import get_user_from_request


@csrf_protect
@require_POST
@login_required
@transaction.atomic
def application_pin_reorder_view(request: HttpRequest) -> JsonResponse:
    """
    AJAX endpoint to reorder pinned applications via drag-and-drop.

    Expects JSON: {"application_ids": [5, 3, 7]}
    Returns: {"success": True}
    """
    try:
        user = get_user_from_request(request=request)
        if user is None:
            return JsonResponse(
                {'success': False, 'error': 'User not authenticated'},
                status=401
            )

        data = json.loads(request.body)
        application_ids = data.get('application_ids', [])

        if not application_ids:
            return JsonResponse(
                {'success': False, 'error': 'application_ids required'},
                status=400
            )

        # Update order based on application IDs
        for index, app_id in enumerate(application_ids):
            ApplicationPin.objects.filter(
                application_id=app_id,
                user=user
            ).update(order=(index + 1) * 10)

        return JsonResponse({'success': True})

    except Exception as e:
        return JsonResponse(
            {'success': False, 'error': str(e)},
            status=400
        )
