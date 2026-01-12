from django.urls import URLPattern, URLResolver, path

from core.views.data_point import (
    data_point_add_view,
    data_point_delete_view,
    data_point_detail_view,
    data_point_edit_view,
    data_point_view,
)

urlpatterns_data_point: list[URLPattern | URLResolver] = [
    path("data_point/", data_point_view, name="data_point"),
    path("data_point/edit/<int:model_id>/", data_point_edit_view, name="data_point_edit"),
    path("data_point/new/", data_point_add_view, name="data_point_new"),
    path("data_point/<int:model_id>/", data_point_detail_view, name="data_point_detail"),
    path("data_point/delete/<int:model_id>/", data_point_delete_view, name="data_point_delete"),
]
