import json

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_POST

from core.models.application import Application
from core.models.procedure_step import ProcedureStep


@require_POST
@login_required
@transaction.atomic
def application_procedure_reorder_view(request: HttpRequest, model_id: int) -> JsonResponse:
    """
    AJAX endpoint to reorder procedure steps.
    Expects JSON: {"step_ids": [3, 1, 2]}  // New order as list of step IDs
    """
    try:
        application = Application.objects.get(id=model_id)
        data = json.loads(request.body)
        step_ids = data.get('step_ids', [])

        # Update order for each step
        for index, step_id in enumerate(step_ids):
            ProcedureStep.objects.filter(
                id=step_id,
                application=application
            ).update(order=(index + 1) * 10)

        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
