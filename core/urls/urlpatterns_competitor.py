from django.urls import URLPattern, URLResolver, path

from core.views.competitor import (
    competitor_add_view,
    competitor_delete_view,
    competitor_detail_view,
    competitor_edit_view,
    competitor_view,
)

urlpatterns_competitor: list[URLPattern | URLResolver] = [
    path("competitor/", competitor_view, name="competitor"),
    path("competitor/edit/<int:model_id>/", competitor_edit_view, name="competitor_edit"),
    path("competitor/new/", competitor_add_view, name="competitor_new"),
    path("competitor/<int:model_id>/", competitor_detail_view, name="competitor_detail"),
    path("competitor/delete/<int:model_id>/", competitor_delete_view, name="competitor_delete"),
]
