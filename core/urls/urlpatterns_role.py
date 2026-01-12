from django.urls import URLPattern, URLResolver, path

from core.views.role import (
    role_add_view,
    role_delete_view,
    role_detail_view,
    role_edit_view,
    role_view,
)

urlpatterns_role: list[URLPattern | URLResolver] = [
    path("role/", role_view, name="role"),
    path("role/edit/<int:model_id>/", role_edit_view, name="role_edit"),
    path("role/new/", role_add_view, name="role_new"),
    path("role/<int:model_id>/", role_detail_view, name="role_detail"),
    path("role/delete/<int:model_id>/", role_delete_view, name="role_delete"),
]
