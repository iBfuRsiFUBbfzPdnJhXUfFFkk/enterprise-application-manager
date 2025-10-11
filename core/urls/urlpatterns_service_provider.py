from django.urls import URLPattern, URLResolver, path

from core.urls.common.create_generic_urlpatterns import create_generic_urlpatterns
from core.views.service_provider import (
    service_provider_add_view,
    service_provider_delete_view,
    service_provider_detail_view,
    service_provider_edit_view,
    service_provider_view,
)

urlpatterns_service_provider: list[URLPattern | URLResolver] = create_generic_urlpatterns(
    name='service_provider',
    view=service_provider_view,
    view_edit=service_provider_edit_view,
    view_new=service_provider_add_view,
)

# Add detail view
urlpatterns_service_provider.append(
    path(name='service_provider_detail', route='service_provider/<int:model_id>/', view=service_provider_detail_view)
)

# Add delete view
urlpatterns_service_provider.append(
    path(name='service_provider_delete', route='service_provider/delete/<int:model_id>/', view=service_provider_delete_view)
)
