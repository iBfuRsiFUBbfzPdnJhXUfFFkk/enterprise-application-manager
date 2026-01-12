from django.urls import URLPattern, URLResolver, path

from core.views.sprint import (
    sprint_add_view,
    sprint_delete_view,
    sprint_detail_view,
    sprint_edit_view,
    sprint_view,
)

urlpatterns_sprint: list[URLPattern | URLResolver] = [
    path("sprint/", sprint_view, name="sprint"),
    path("sprint/edit/<int:model_id>/", sprint_edit_view, name="sprint_edit"),
    path("sprint/new/", sprint_add_view, name="sprint_new"),
    path("sprint/<int:model_id>/", sprint_detail_view, name="sprint_detail"),
    path("sprint/delete/<int:model_id>/", sprint_delete_view, name="sprint_delete"),
]
