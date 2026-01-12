from django.urls import URLPattern, URLResolver, path

from core.views.ai_use_case import (
    ai_use_case_add_view,
    ai_use_case_delete_view,
    ai_use_case_detail_view,
    ai_use_case_edit_view,
    ai_use_case_view,
)

urlpatterns_ai_use_case: list[URLPattern | URLResolver] = [
    path("ai_use_case/", ai_use_case_view, name="ai_use_case"),
    path("ai_use_case/edit/<int:model_id>/", ai_use_case_edit_view, name="ai_use_case_edit"),
    path("ai_use_case/new/", ai_use_case_add_view, name="ai_use_case_new"),
    path("ai-use-case/<int:model_id>/", ai_use_case_detail_view, name="ai_use_case_detail"),
    path("ai-use-case/delete/<int:model_id>/", ai_use_case_delete_view, name="ai_use_case_delete"),
]
