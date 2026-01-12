from django.urls import URLPattern, URLResolver, path

from core.views.server import (
    server_add_view,
    server_delete_view,
    server_detail_view,
    server_edit_view,
    server_view,
)

urlpatterns_server: list[URLPattern | URLResolver] = [
    path("server/", server_view, name="server"),
    path("server/edit/<int:model_id>/", server_edit_view, name="server_edit"),
    path("server/new/", server_add_view, name="server_new"),
    path("server/<int:model_id>/", server_detail_view, name="server_detail"),
    path("server/delete/<int:model_id>/", server_delete_view, name="server_delete"),
]
