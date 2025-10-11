from django.urls import URLPattern, URLResolver, path

from core.urls.common.create_generic_urlpatterns import create_generic_urlpatterns
from core.views.project import (
    project_add_view,
    project_delete_view,
    project_detail_view,
    project_edit_view,
    project_view,
)

urlpatterns_project: list[URLPattern | URLResolver] = create_generic_urlpatterns(
    name='project',
    view=project_view,
    view_edit=project_edit_view,
    view_new=project_add_view,
)

# Add detail view
urlpatterns_project.append(
    path(name='project_detail', route='project/<int:model_id>/', view=project_detail_view)
)

# Add delete view
urlpatterns_project.append(
    path(name='project_delete', route='project/delete/<int:model_id>/', view=project_delete_view)
)
