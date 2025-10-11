from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.task_form import TaskForm
from core.models.task import Task
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def task_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        task = Task.objects.get(id=model_id)
    except Task.DoesNotExist:
        return generic_500(request=request)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task')
    else:
        form = TaskForm(instance=task)

    return base_render(
        request=request,
        template_name='authenticated/task/task_form.html',
        context={'form': form}
    )
