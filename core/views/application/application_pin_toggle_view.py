import json

from django.contrib.auth.decorators import login_required
from django.db import models, transaction
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_POST

from core.models.application import Application
from core.models.application_pin import ApplicationPin
from core.utilities.get_user_from_request import get_user_from_request


@require_POST
@login_required
@transaction.atomic
def application_pin_toggle_view(request: HttpRequest) -> JsonResponse:
    """
    AJAX endpoint to toggle pin status for an application.

    Expects JSON: {"application_id": 123}
    Returns: {"success": True, "pinned": True/False}
    """
    try:
        user = get_user_from_request(request=request)
        if user is None:
            return JsonResponse(
                {'success': False, 'error': 'User not authenticated'},
                status=401
            )

        data = json.loads(request.body)
        application_id = data.get('application_id')

        if not application_id:
            return JsonResponse(
                {'success': False, 'error': 'application_id required'},
                status=400
            )

        application = Application.objects.get(id=application_id)
        existing_pin = ApplicationPin.objects.filter(
            user=user,
            application=application
        ).first()

        if existing_pin:
            existing_pin.delete()
            return JsonResponse({
                'success': True,
                'pinned': False,
                'application_id': application_id
            })
        else:
            max_order = ApplicationPin.objects.filter(user=user).aggregate(
                models.Max('order')
            )['order__max'] or 0

            new_pin = ApplicationPin.objects.create(
                user=user,
                application=application,
                order=max_order + 10
            )

            return JsonResponse({
                'success': True,
                'pinned': True,
                'application_id': application_id,
                'order': new_pin.order
            })

    except Application.DoesNotExist:
        return JsonResponse(
            {'success': False, 'error': 'Application not found'},
            status=404
        )
    except Exception as e:
        return JsonResponse(
            {'success': False, 'error': str(e)},
            status=400
        )
