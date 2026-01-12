from django.urls import URLPattern, URLResolver, path

from core.views.ai_governance import (
    ai_governance_add_view,
    ai_governance_delete_view,
    ai_governance_detail_view,
    ai_governance_edit_view,
    ai_governance_view,
)

urlpatterns_ai_governance: list[URLPattern | URLResolver] = [
    path("ai_governance/", ai_governance_view, name="ai_governance"),
    path("ai_governance/edit/<int:model_id>/", ai_governance_edit_view, name="ai_governance_edit"),
    path("ai_governance/new/", ai_governance_add_view, name="ai_governance_new"),
    path("ai-governance/<int:model_id>/", ai_governance_detail_view, name="ai_governance_detail"),
    path("ai-governance/delete/<int:model_id>/", ai_governance_delete_view, name="ai_governance_delete"),
]
