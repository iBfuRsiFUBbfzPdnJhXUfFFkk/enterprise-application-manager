from django.urls import URLPattern, URLResolver, path

from core.urls.common.create_generic_urlpatterns import create_generic_urlpatterns
from core.views.incident import (
    incident_add_view,
    incident_delete_view,
    incident_detail_view,
    incident_edit_view,
    incident_view,
)

urlpatterns_incident: list[URLPattern | URLResolver] = create_generic_urlpatterns(
    name='incident',
    view=incident_view,
    view_edit=incident_edit_view,
    view_new=incident_add_view,
)

# Add detail view
urlpatterns_incident.append(
    path(name='incident_detail', route='incident/<int:model_id>/', view=incident_detail_view)
)

# Add delete view
urlpatterns_incident.append(
    path(name='incident_delete', route='incident/delete/<int:model_id>/', view=incident_delete_view)
)
