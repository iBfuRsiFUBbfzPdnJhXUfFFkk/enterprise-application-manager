from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.task_form import TaskForm
from core.utilities.base_render import base_render


def task_add_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task')
    else:
        form = TaskForm()

    return base_render(
        request=request,
        template_name='authenticated/task/task_form.html',
        context={'form': form}
    )
