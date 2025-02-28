from django.urls import URLPattern, URLResolver, path

from core.views.acronym.acronym_add_view import acronym_add_view
from core.views.acronym.acronym_edit_view import acronym_edit_view
from core.views.acronym.acronym_view import acronym_view

urlpatterns_acronym: list[URLPattern | URLResolver] = [
    path(name="acronym", route="acronym", view=acronym_view),
    path(name="acronym_new", route="acronym/new", view=acronym_add_view),
    path(name="acronym_edit", route="acronym/edit/<int:model_id>", view=acronym_edit_view),
]
