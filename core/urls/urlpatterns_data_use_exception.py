from django.urls import URLPattern, URLResolver, path

from core.views.data_use_exception import (
    data_use_exception_add_view,
    data_use_exception_delete_view,
    data_use_exception_detail_view,
    data_use_exception_edit_view,
    data_use_exception_view,
)

urlpatterns_data_use_exception: list[URLPattern | URLResolver] = [
    path("data_use_exception/", data_use_exception_view, name="data_use_exception"),
    path("data_use_exception/edit/<int:model_id>/", data_use_exception_edit_view, name="data_use_exception_edit"),
    path("data_use_exception/new/", data_use_exception_add_view, name="data_use_exception_new"),
    path("data_use_exception/<int:model_id>/", data_use_exception_detail_view, name="data_use_exception_detail"),
    path("data_use_exception/delete/<int:model_id>/", data_use_exception_delete_view, name="data_use_exception_delete"),
]
