from django.urls import URLPattern, URLResolver, path

from core.views.service_provider_security_requirements_document import (
    service_provider_security_requirements_document_add_view,
    service_provider_security_requirements_document_delete_view,
    service_provider_security_requirements_document_detail_view,
    service_provider_security_requirements_document_edit_view,
    service_provider_security_requirements_document_view,
)

urlpatterns_service_provider_security_requirements_document: list[URLPattern | URLResolver] = [
    path("service_provider_security_requirements_document/", service_provider_security_requirements_document_view, name="service_provider_security_requirements_document"),
    path("service_provider_security_requirements_document/edit/<int:model_id>/", service_provider_security_requirements_document_edit_view, name="service_provider_security_requirements_document_edit"),
    path("service_provider_security_requirements_document/new/", service_provider_security_requirements_document_add_view, name="service_provider_security_requirements_document_new"),
    path("service_provider_security_requirements_document/<int:model_id>/", service_provider_security_requirements_document_detail_view, name="service_provider_security_requirements_document_detail"),
    path("service_provider_security_requirements_document/delete/<int:model_id>/", service_provider_security_requirements_document_delete_view, name="service_provider_security_requirements_document_delete"),
]
