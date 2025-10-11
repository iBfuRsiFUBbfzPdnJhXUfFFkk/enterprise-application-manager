from django.http import HttpRequest, HttpResponse

from core.models.task import Task
from core.views.generic.generic_view import generic_view


def task_view(request: HttpRequest) -> HttpResponse:
    return generic_view(
        model_cls=Task,
        name='task',
        request=request,
    )
