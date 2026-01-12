from django.urls import URLPattern, URLResolver, path

from core.views.acronym.acronym_add_view import acronym_add_view
from core.views.acronym.acronym_delete_view import acronym_delete_view
from core.views.acronym.acronym_detail_view import acronym_detail_view
from core.views.acronym.acronym_edit_view import acronym_edit_view
from core.views.acronym.acronym_view import acronym_view

urlpatterns_acronym: list[URLPattern | URLResolver] = [
    path("acronym/", acronym_view, name="acronym"),
    path("acronym/edit/<int:model_id>/", acronym_edit_view, name="acronym_edit"),
    path("acronym/new/", acronym_add_view, name="acronym_new"),
    path("acronym/<int:model_id>/", acronym_detail_view, name="acronym_detail"),
    path("acronym/delete/<int:model_id>/", acronym_delete_view, name="acronym_delete"),
]
