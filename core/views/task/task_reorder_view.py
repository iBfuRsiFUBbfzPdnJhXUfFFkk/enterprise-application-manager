import json

from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_POST

from core.models.task import Task


@require_POST
def task_reorder_view(request: HttpRequest) -> JsonResponse:
    """Update task order based on drag and drop"""
    try:
        data = json.loads(request.body)
        task_orders = data.get('task_orders', [])

        # Update each task's order
        for item in task_orders:
            task_id = item.get('id')
            new_order = item.get('order')

            if task_id and new_order is not None:
                Task.objects.filter(id=task_id).update(order=new_order)

        return JsonResponse({'status': 'success'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
