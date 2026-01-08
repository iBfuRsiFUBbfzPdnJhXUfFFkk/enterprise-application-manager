from django.urls import URLPattern, URLResolver, path

from core.urls.common.create_generic_urlpatterns import create_generic_urlpatterns
from core.views.hr_incident import (
    hr_incident_add_update_view,
    hr_incident_add_view,
    hr_incident_delete_view,
    hr_incident_detail_view,
    hr_incident_download_update_attachment_view,
    hr_incident_edit_view,
    hr_incident_view,
)

urlpatterns_hr_incident: list[URLPattern | URLResolver] = create_generic_urlpatterns(
    name='hr_incident',
    view=hr_incident_view,
    view_edit=hr_incident_edit_view,
    view_new=hr_incident_add_view,
)

# Add detail view
urlpatterns_hr_incident.append(
    path(name='hr_incident_detail', route='hr-incident/<int:model_id>/', view=hr_incident_detail_view)
)

# Add delete view
urlpatterns_hr_incident.append(
    path(name='hr_incident_delete', route='hr-incident/delete/<int:model_id>/', view=hr_incident_delete_view)
)

# Add update views
urlpatterns_hr_incident.append(
    path(name='hr_incident_add_update', route='hr-incident/<int:model_id>/add-update/', view=hr_incident_add_update_view)
)

urlpatterns_hr_incident.append(
    path(name='hr_incident_download_update_attachment', route='hr-incident/update/<int:update_id>/download-attachment/', view=hr_incident_download_update_attachment_view)
)
