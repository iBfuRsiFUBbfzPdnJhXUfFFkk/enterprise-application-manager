from django.urls import URLPattern, URLResolver, path

from core.views.maintenance_window import (
    maintenance_window_add_view,
    maintenance_window_delete_view,
    maintenance_window_detail_view,
    maintenance_window_edit_view,
    maintenance_window_view,
)

urlpatterns_maintenance_window: list[URLPattern | URLResolver] = [
    path("maintenance_window/", maintenance_window_view, name="maintenance_window"),
    path("maintenance_window/edit/<int:model_id>/", maintenance_window_edit_view, name="maintenance_window_edit"),
    path("maintenance_window/new/", maintenance_window_add_view, name="maintenance_window_new"),
    path("maintenance-window/<int:model_id>/", maintenance_window_detail_view, name="maintenance_window_detail"),
    path("maintenance-window/delete/<int:model_id>/", maintenance_window_delete_view, name="maintenance_window_delete"),
]
