from django.urls import URLPattern, URLResolver, path

from core.views.term import (
    term_add_view,
    term_delete_view,
    term_detail_view,
    term_edit_view,
    term_view,
)

urlpatterns_term: list[URLPattern | URLResolver] = [
    path("term/", term_view, name="term"),
    path("term/edit/<int:model_id>/", term_edit_view, name="term_edit"),
    path("term/new/", term_add_view, name="term_new"),
    path("term/<int:model_id>/", term_detail_view, name="term_detail"),
    path("term/delete/<int:model_id>/", term_delete_view, name="term_delete"),
]
