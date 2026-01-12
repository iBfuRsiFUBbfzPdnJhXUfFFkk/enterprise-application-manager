from django.urls import URLPattern, URLResolver, path

from core.views.client import (
    client_add_view,
    client_delete_view,
    client_detail_view,
    client_edit_view,
    client_view,
)

urlpatterns_client: list[URLPattern | URLResolver] = [
    path("client/", client_view, name="client"),
    path("client/edit/<int:model_id>/", client_edit_view, name="client_edit"),
    path("client/new/", client_add_view, name="client_new"),
    path("client/<int:model_id>/", client_detail_view, name="client_detail"),
    path("client/delete/<int:model_id>/", client_delete_view, name="client_delete"),
]
