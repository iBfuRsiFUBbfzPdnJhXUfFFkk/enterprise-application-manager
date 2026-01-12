from django.urls import URLPattern, URLResolver, path

from core.views.service_provider import (
    service_provider_add_view,
    service_provider_delete_view,
    service_provider_detail_view,
    service_provider_edit_view,
    service_provider_view,
)

urlpatterns_service_provider: list[URLPattern | URLResolver] = [
    path("service_provider/", service_provider_view, name="service_provider"),
    path("service_provider/edit/<int:model_id>/", service_provider_edit_view, name="service_provider_edit"),
    path("service_provider/new/", service_provider_add_view, name="service_provider_new"),
    path("service_provider/<int:model_id>/", service_provider_detail_view, name="service_provider_detail"),
    path("service_provider/delete/<int:model_id>/", service_provider_delete_view, name="service_provider_delete"),
]
