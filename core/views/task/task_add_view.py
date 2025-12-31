from django.db.models import Max
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.task_form import TaskForm
from core.models.task import Task
from core.utilities.base_render import base_render


def task_add_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            # If no order is set, put it at the end
            if task.order is None:
                max_order = Task.objects.aggregate(Max('order'))['order__max']
                task.order = (max_order or 0) + 1
            task.save()
            return redirect('task')
    else:
        form = TaskForm()

    return base_render(
        request=request,
        template_name='authenticated/task/task_form.html',
        context={'form': form}
    )
