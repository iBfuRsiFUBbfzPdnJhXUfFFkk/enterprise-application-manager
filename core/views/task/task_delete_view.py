from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.models.task import Task
from core.views.generic.generic_500 import generic_500


def task_delete_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        task = Task.objects.get(id=model_id)
        task.delete()
    except Task.DoesNotExist:
        return generic_500(request=request)

    return redirect('task')
