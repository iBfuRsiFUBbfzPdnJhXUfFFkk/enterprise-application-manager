from django.urls import URLPattern, URLResolver, path

from core.views.secret import (
    secret_add_view,
    secret_detail_view,
    secret_edit_view,
    secret_quick_add_view,
    secret_view,
)

urlpatterns_secret: list[URLPattern | URLResolver] = [
    path("secret/", secret_view, name="secret"),
    path("secret/detail/<int:model_id>/", secret_detail_view, name="secret_detail"),
    path("secret/edit/<int:model_id>/", secret_edit_view, name="secret_edit"),
    path("secret/new/", secret_add_view, name="secret_new"),
    path("secret/quick-add/", secret_quick_add_view, name="secret_quick_add"),
]
