from django.urls import URLPattern, URLResolver, path

from core.views.it_devops_request.it_devops_request_add_view import it_devops_request_add_view
from core.views.it_devops_request.it_devops_request_complete_view import it_devops_request_complete_view
from core.views.it_devops_request.it_devops_request_detail_view import it_devops_request_detail_view
from core.views.it_devops_request.it_devops_request_edit_view import it_devops_request_edit_view
from core.views.it_devops_request.it_devops_request_export_docx_view import it_devops_request_export_docx_view
from core.views.it_devops_request.it_devops_request_export_pdf_view import it_devops_request_export_pdf_view
from core.views.it_devops_request.it_devops_request_update_add_ajax_view import it_devops_request_update_add_ajax_view
from core.views.it_devops_request.it_devops_request_update_delete_ajax_view import it_devops_request_update_delete_ajax_view
from core.views.it_devops_request.it_devops_request_update_edit_ajax_view import it_devops_request_update_edit_ajax_view
from core.views.it_devops_request.it_devops_request_view import it_devops_request_view


urlpatterns_it_devops_request: list[URLPattern | URLResolver] = [
    path("it_devops_request/", it_devops_request_view, name="it_devops_request"),
    path("it_devops_request/edit/<int:model_id>/", it_devops_request_edit_view, name="it_devops_request_edit"),
    path("it_devops_request/new/", it_devops_request_add_view, name="it_devops_request_new"),
    path("it-devops-request/<int:model_id>/detail/", it_devops_request_detail_view, name="it_devops_request_detail"),
    path("it-devops-request/export/docx/", it_devops_request_export_docx_view, name="it_devops_request_export_docx"),
    path("it-devops-request/export/pdf/", it_devops_request_export_pdf_view, name="it_devops_request_export_pdf"),
    path("it-devops-request/<int:model_id>/update/add/", it_devops_request_update_add_ajax_view, name="it_devops_request_update_add"),
    path("it-devops-request/update/<int:update_id>/edit/", it_devops_request_update_edit_ajax_view, name="it_devops_request_update_edit"),
    path("it-devops-request/update/<int:update_id>/delete/", it_devops_request_update_delete_ajax_view, name="it_devops_request_update_delete"),
    path("it-devops-request/<int:model_id>/complete/", it_devops_request_complete_view, name="it_devops_request_complete"),
]
