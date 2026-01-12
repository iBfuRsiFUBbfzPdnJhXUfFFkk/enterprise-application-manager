from django.urls import URLPattern, URLResolver, path

from core.views.incident import (
    incident_add_view,
    incident_delete_view,
    incident_detail_view,
    incident_edit_view,
    incident_view,
)

urlpatterns_incident: list[URLPattern | URLResolver] = [
    path("incident/", incident_view, name="incident"),
    path("incident/edit/<int:model_id>/", incident_edit_view, name="incident_edit"),
    path("incident/new/", incident_add_view, name="incident_new"),
    path("incident/<int:model_id>/", incident_detail_view, name="incident_detail"),
    path("incident/delete/<int:model_id>/", incident_delete_view, name="incident_delete"),
]
