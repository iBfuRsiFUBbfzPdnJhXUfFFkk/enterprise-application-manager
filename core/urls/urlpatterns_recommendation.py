from django.urls import URLPattern, URLResolver, path

from core.views.recommendation.recommendation_add_view import recommendation_add_view
from core.views.recommendation.recommendation_detail_view import recommendation_detail_view
from core.views.recommendation.recommendation_edit_view import recommendation_edit_view
from core.views.recommendation.recommendation_export_docx_view import recommendation_export_docx_view
from core.views.recommendation.recommendation_view import recommendation_view


urlpatterns_recommendation: list[URLPattern | URLResolver] = [
    path("recommendation/", recommendation_view, name="recommendation"),
    path("recommendation/edit/<int:model_id>/", recommendation_edit_view, name="recommendation_edit"),
    path("recommendation/new/", recommendation_add_view, name="recommendation_new"),
    path("recommendation/<int:model_id>/detail/", recommendation_detail_view, name="recommendation_detail"),
    path("recommendation/export/docx/", recommendation_export_docx_view, name="recommendation_export_docx"),
]
