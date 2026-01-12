from django.urls import URLPattern, URLResolver, path

from core.views.hr_incident import (
    hr_incident_add_update_view,
    hr_incident_add_view,
    hr_incident_delete_view,
    hr_incident_detail_view,
    hr_incident_edit_view,
    hr_incident_view,
)

urlpatterns_hr_incident: list[URLPattern | URLResolver] = [
    path("hr_incident/", hr_incident_view, name="hr_incident"),
    path("hr_incident/edit/<int:model_id>/", hr_incident_edit_view, name="hr_incident_edit"),
    path("hr_incident/new/", hr_incident_add_view, name="hr_incident_new"),
    path("hr-incident/<int:model_id>/", hr_incident_detail_view, name="hr_incident_detail"),
    path("hr-incident/delete/<int:model_id>/", hr_incident_delete_view, name="hr_incident_delete"),
    path("hr-incident/<int:model_id>/add-update/", hr_incident_add_update_view, name="hr_incident_add_update"),
]
