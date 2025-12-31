from datetime import date

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect

from core.models.common.enums.task_status_choices import TASK_STATUS_COMPLETED
from core.models.task import Task


def task_complete_view(request: HttpRequest, model_id: int) -> HttpResponse:
    """Mark a task as complete"""
    if request.method != "POST":
        return redirect('task_detail', model_id=model_id)

    task: Task = get_object_or_404(Task, id=model_id)

    # Mark as completed
    task.status = TASK_STATUS_COMPLETED
    task.date_completed = date.today()
    task.save()

    messages.success(request, f"Task '{task.name}' marked as complete!")

    # Redirect back to referring page (list or detail)
    referer = request.META.get('HTTP_REFERER', '')
    if 'task/' in referer and str(model_id) in referer:
        # Came from detail page
        return redirect('task_detail', model_id=model_id)
    else:
        # Came from list page
        return redirect('task')
