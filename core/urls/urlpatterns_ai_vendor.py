from django.urls import URLPattern, URLResolver, path

from core.views.ai_vendor import (
    ai_vendor_add_view,
    ai_vendor_delete_view,
    ai_vendor_detail_view,
    ai_vendor_edit_view,
    ai_vendor_view,
)

urlpatterns_ai_vendor: list[URLPattern | URLResolver] = [
    path("ai_vendor/", ai_vendor_view, name="ai_vendor"),
    path("ai_vendor/edit/<int:model_id>/", ai_vendor_edit_view, name="ai_vendor_edit"),
    path("ai_vendor/new/", ai_vendor_add_view, name="ai_vendor_new"),
    path("ai-vendor/<int:model_id>/", ai_vendor_detail_view, name="ai_vendor_detail"),
    path("ai-vendor/delete/<int:model_id>/", ai_vendor_delete_view, name="ai_vendor_delete"),
]
