from django.http import HttpRequest, HttpResponse

from core.models.task import Task
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def task_detail_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        task = Task.objects.get(id=model_id)
        historical_records = task.history.all()
    except Task.DoesNotExist:
        return generic_500(request=request)

    return base_render(
        request=request,
        template_name='authenticated/task/task_detail.html',
        context={
            'task': task,
            'historical_records': historical_records,
        }
    )
