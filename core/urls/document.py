from django.urls import URLPattern, URLResolver, path

from core.views.document.document_add_view import document_add_view
from core.views.document.document_edit_view import document_edit_view
from core.views.document.document_view import document_view

urlpatterns_document: list[URLPattern | URLResolver] = [
    path(name="document", route="document", view=document_view),
    path(name="document_new", route="document/new", view=document_add_view),
    path(name="document_edit", route="document/edit/<int:model_id>", view=document_edit_view),
]
