from django.urls import URLPattern, URLResolver, path

from core.views.requirement import (
    requirement_add_view,
    requirement_delete_view,
    requirement_detail_view,
    requirement_edit_view,
    requirement_view,
)

urlpatterns_requirement: list[URLPattern | URLResolver] = [
    path("requirement/", requirement_view, name="requirement"),
    path("requirement/edit/<int:model_id>/", requirement_edit_view, name="requirement_edit"),
    path("requirement/new/", requirement_add_view, name="requirement_new"),
    path("requirement/<int:model_id>/", requirement_detail_view, name="requirement_detail"),
    path("requirement/delete/<int:model_id>/", requirement_delete_view, name="requirement_delete"),
]
