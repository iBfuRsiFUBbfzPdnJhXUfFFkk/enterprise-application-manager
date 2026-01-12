from django.urls import URLPattern, URLResolver, path

from core.views.task import (
    task_add_view,
    task_complete_view,
    task_delete_view,
    task_detail_view,
    task_edit_view,
    task_reorder_view,
    task_view,
)

urlpatterns_task: list[URLPattern | URLResolver] = [
    path("task/", task_view, name="task"),
    path("task/edit/<int:model_id>/", task_edit_view, name="task_edit"),
    path("task/new/", task_add_view, name="task_new"),
    path("task/<int:model_id>/", task_detail_view, name="task_detail"),
    path("task/delete/<int:model_id>/", task_delete_view, name="task_delete"),
    path("task/complete/<int:model_id>/", task_complete_view, name="task_complete"),
    path("task/reorder/", task_reorder_view, name="task_reorder"),
]
