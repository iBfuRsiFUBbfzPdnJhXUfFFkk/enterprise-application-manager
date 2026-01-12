from django.urls import URLPattern, URLResolver, path

from core.views.project import (
    project_add_view,
    project_delete_view,
    project_detail_view,
    project_edit_view,
    project_view,
)

urlpatterns_project: list[URLPattern | URLResolver] = [
    path("project/", project_view, name="project"),
    path("project/edit/<int:model_id>/", project_edit_view, name="project_edit"),
    path("project/new/", project_add_view, name="project_new"),
    path("project/<int:model_id>/", project_detail_view, name="project_detail"),
    path("project/delete/<int:model_id>/", project_delete_view, name="project_delete"),
]
