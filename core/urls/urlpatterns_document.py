from django.urls import URLPattern, URLResolver, path

from core.urls.common.create_generic_urlpatterns import create_generic_urlpatterns
from core.views.document.document_add_view import document_add_view
from core.views.document.document_create_ajax_view import document_create_ajax_view
from core.views.document.document_detail_view import document_detail_view
from core.views.document.document_edit_view import document_edit_view
from core.views.document.document_view import document_view

urlpatterns_document: list[URLPattern | URLResolver] = create_generic_urlpatterns(
    name="document",
    view=document_view,
    view_edit=document_edit_view,
    view_new=document_add_view,
)

# Add detail view
urlpatterns_document.append(
    path(name='document_detail', route='document/detail/<int:model_id>/', view=document_detail_view)
)

# Add AJAX create view
urlpatterns_document.append(
    path(name='document_create_ajax', route='document/create/ajax/', view=document_create_ajax_view)
)
