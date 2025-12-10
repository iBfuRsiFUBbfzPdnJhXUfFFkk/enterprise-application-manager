from django.urls import URLPattern, URLResolver, path

from core.urls.common.create_generic_urlpatterns import create_generic_urlpatterns
from core.views.recommendation.recommendation_add_view import recommendation_add_view
from core.views.recommendation.recommendation_detail_view import recommendation_detail_view
from core.views.recommendation.recommendation_edit_view import recommendation_edit_view
from core.views.recommendation.recommendation_export_docx_view import recommendation_export_docx_view
from core.views.recommendation.recommendation_view import recommendation_view


urlpatterns_recommendation: list[URLPattern | URLResolver] = create_generic_urlpatterns(
    name="recommendation",
    view=recommendation_view,
    view_edit=recommendation_edit_view,
    view_new=recommendation_add_view,
)

urlpatterns_recommendation.extend(
    [
        path(
            route="recommendation/<int:model_id>/detail/",
            view=recommendation_detail_view,
            name="recommendation_detail",
        ),
        path(
            route="recommendation/export/docx/",
            view=recommendation_export_docx_view,
            name="recommendation_export_docx",
        ),
    ]
)
