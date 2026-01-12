from django.urls import URLPattern, URLResolver, path

from core.views.risk import (
    risk_add_view,
    risk_delete_view,
    risk_detail_view,
    risk_edit_view,
    risk_view,
)

urlpatterns_risk: list[URLPattern | URLResolver] = [
    path("risk/", risk_view, name="risk"),
    path("risk/edit/<int:model_id>/", risk_edit_view, name="risk_edit"),
    path("risk/new/", risk_add_view, name="risk_new"),
    path("risk/<int:model_id>/", risk_detail_view, name="risk_detail"),
    path("risk/delete/<int:model_id>/", risk_delete_view, name="risk_delete"),
]
