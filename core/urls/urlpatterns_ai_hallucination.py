from django.urls import URLPattern, URLResolver, path

from core.views.ai_hallucination import (
    ai_hallucination_add_view,
    ai_hallucination_delete_view,
    ai_hallucination_detail_view,
    ai_hallucination_edit_view,
    ai_hallucination_view,
)

urlpatterns_ai_hallucination: list[URLPattern | URLResolver] = [
    path("ai_hallucination/", ai_hallucination_view, name="ai_hallucination"),
    path("ai_hallucination/edit/<int:model_id>/", ai_hallucination_edit_view, name="ai_hallucination_edit"),
    path("ai_hallucination/new/", ai_hallucination_add_view, name="ai_hallucination_new"),
    path("ai-hallucination/<int:model_id>/", ai_hallucination_detail_view, name="ai_hallucination_detail"),
    path("ai-hallucination/delete/<int:model_id>/", ai_hallucination_delete_view, name="ai_hallucination_delete"),
]
