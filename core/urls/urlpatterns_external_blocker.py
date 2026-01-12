from django.urls import URLPattern, URLResolver, path

from core.views.external_blocker import (
    external_blocker_add_view,
    external_blocker_delete_view,
    external_blocker_detail_view,
    external_blocker_edit_view,
    external_blocker_view,
)

urlpatterns_external_blocker: list[URLPattern | URLResolver] = [
    path("external_blocker/", external_blocker_view, name="external_blocker"),
    path("external_blocker/edit/<int:model_id>/", external_blocker_edit_view, name="external_blocker_edit"),
    path("external_blocker/new/", external_blocker_add_view, name="external_blocker_new"),
    path("external_blocker/<int:model_id>/", external_blocker_detail_view, name="external_blocker_detail"),
    path("external_blocker/delete/<int:model_id>/", external_blocker_delete_view, name="external_blocker_delete"),
]
