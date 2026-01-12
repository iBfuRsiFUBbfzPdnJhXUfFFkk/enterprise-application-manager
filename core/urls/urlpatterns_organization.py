from django.urls import URLPattern, URLResolver, path

from core.views.organization import (
    organization_add_view,
    organization_delete_view,
    organization_detail_view,
    organization_edit_view,
    organization_view,
)

urlpatterns_organization: list[URLPattern | URLResolver] = [
    path("organization/", organization_view, name="organization"),
    path("organization/edit/<int:model_id>/", organization_edit_view, name="organization_edit"),
    path("organization/new/", organization_add_view, name="organization_new"),
    path("organization/<int:model_id>/", organization_detail_view, name="organization_detail"),
    path("organization/delete/<int:model_id>/", organization_delete_view, name="organization_delete"),
]
