from django.urls import URLPattern, URLResolver

from core.urls.common.create_generic_urlpatterns import create_generic_urlpatterns
from core.views.document.document_add_view import document_add_view
from core.views.document.document_edit_view import document_edit_view
from core.views.document.document_view import document_view

urlpatterns_document: list[URLPattern | URLResolver] = create_generic_urlpatterns(
    name="document",
    view=document_view,
    view_edit=document_edit_view,
    view_new=document_add_view,
)
