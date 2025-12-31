from django.urls import URLPattern, URLResolver, path

from core.urls.common.create_generic_urlpatterns import create_generic_urlpatterns
from core.views.task import (
    task_add_view,
    task_complete_view,
    task_delete_view,
    task_detail_view,
    task_edit_view,
    task_reorder_view,
    task_view,
)

urlpatterns_task: list[URLPattern | URLResolver] = create_generic_urlpatterns(
    name='task',
    view=task_view,
    view_edit=task_edit_view,
    view_new=task_add_view,
)

# Add detail view
urlpatterns_task.append(
    path(name='task_detail', route='task/<int:model_id>/', view=task_detail_view)
)

# Add delete view
urlpatterns_task.append(
    path(name='task_delete', route='task/delete/<int:model_id>/', view=task_delete_view)
)

# Add quick complete action
urlpatterns_task.append(
    path(name='task_complete', route='task/complete/<int:model_id>/', view=task_complete_view)
)

# Add reorder action
urlpatterns_task.append(
    path(name='task_reorder', route='task/reorder/', view=task_reorder_view)
)
