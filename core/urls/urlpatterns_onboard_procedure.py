from django.urls import URLPattern, URLResolver, path

from core.views.onboard_procedure import (
    onboard_procedure_add_view,
    onboard_procedure_delete_view,
    onboard_procedure_detail_view,
    onboard_procedure_edit_view,
    onboard_procedure_view,
)

urlpatterns_onboard_procedure: list[URLPattern | URLResolver] = [
    path("onboard_procedure/", onboard_procedure_view, name="onboard_procedure"),
    path("onboard_procedure/edit/<int:model_id>/", onboard_procedure_edit_view, name="onboard_procedure_edit"),
    path("onboard_procedure/new/", onboard_procedure_add_view, name="onboard_procedure_new"),
    path("onboard_procedure/<int:model_id>/", onboard_procedure_detail_view, name="onboard_procedure_detail"),
    path("onboard_procedure/delete/<int:model_id>/", onboard_procedure_delete_view, name="onboard_procedure_delete"),
]
