from django.urls import URLPattern, URLResolver, path

from core.urls.common.create_generic_urlpatterns import create_generic_urlpatterns
from core.views.service_provider_security_requirements_document import (
    service_provider_security_requirements_document_add_view,
    service_provider_security_requirements_document_delete_view,
    service_provider_security_requirements_document_detail_view,
    service_provider_security_requirements_document_edit_view,
    service_provider_security_requirements_document_view,
)

urlpatterns_service_provider_security_requirements_document: list[URLPattern | URLResolver] = create_generic_urlpatterns(
    name='service_provider_security_requirements_document',
    view=service_provider_security_requirements_document_view,
    view_edit=service_provider_security_requirements_document_edit_view,
    view_new=service_provider_security_requirements_document_add_view,
)

# Add detail view
urlpatterns_service_provider_security_requirements_document.append(
    path(name='service_provider_security_requirements_document_detail', route='service_provider_security_requirements_document/<int:model_id>/', view=service_provider_security_requirements_document_detail_view)
)

# Add delete view
urlpatterns_service_provider_security_requirements_document.append(
    path(name='service_provider_security_requirements_document_delete', route='service_provider_security_requirements_document/delete/<int:model_id>/', view=service_provider_security_requirements_document_delete_view)
)
