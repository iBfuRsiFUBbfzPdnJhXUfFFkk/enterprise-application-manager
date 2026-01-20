from django.urls import URLPattern, URLResolver, path

from core.views.proposal.proposal_add_view import proposal_add_view
from core.views.proposal.proposal_detail_view import proposal_detail_view
from core.views.proposal.proposal_edit_view import proposal_edit_view
from core.views.proposal.proposal_export_docx_view import proposal_export_docx_view
from core.views.proposal.proposal_export_pdf_view import proposal_export_pdf_view
from core.views.proposal.proposal_update_add_ajax_view import proposal_update_add_ajax_view
from core.views.proposal.proposal_view import proposal_view


urlpatterns_proposal: list[URLPattern | URLResolver] = [
    path("proposal/", proposal_view, name="proposal"),
    path("proposal/edit/<int:model_id>/", proposal_edit_view, name="proposal_edit"),
    path("proposal/new/", proposal_add_view, name="proposal_new"),
    path("proposal/<int:model_id>/detail/", proposal_detail_view, name="proposal_detail"),
    path("proposal/export/docx/", proposal_export_docx_view, name="proposal_export_docx"),
    path("proposal/export/pdf/", proposal_export_pdf_view, name="proposal_export_pdf"),
    path("proposal/<int:model_id>/update/add/", proposal_update_add_ajax_view, name="proposal_update_add"),
]
