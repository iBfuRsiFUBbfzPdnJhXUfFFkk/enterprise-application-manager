from datetime import datetime, timezone
from io import BytesIO

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from docx import Document

from core.models.proposal import Proposal
from core.views.generic.generic_500 import generic_500
from core.views.proposal.utilities.proposal_docx_helpers import (
    add_attachments_section,
    add_header_footer,
    add_links_section,
    add_proposal_intro,
    add_proposal_section,
    add_updates_section,
    set_narrow_margins,
)


@login_required
def proposal_export_docx_view(request: HttpRequest) -> HttpResponse:
    """Export selected proposal to DOCX document."""
    try:
        selected_ids = request.GET.get("ids", "").split(",")
        selected_ids = [int(id) for id in selected_ids if id.strip().isdigit()]

        if not selected_ids or len(selected_ids) != 1:
            return generic_500(request=request)

        try:
            proposal = Proposal.objects.select_related(
                "application",
                "project",
                "person_author",
                "person_reviewer",
                "person_approver",
            ).prefetch_related(
                "attachments",
                "links",
                "updates__person_author",
            ).get(id=selected_ids[0])
        except Proposal.DoesNotExist:
            return generic_500(request=request)

        now = datetime.now(timezone.utc)
        date_str = now.strftime("%Y-%m-%d %I:%M %p UTC")

        document = Document()
        set_narrow_margins(document)

        person_name = ""
        if proposal.person_author:
            person = proposal.person_author
            person_name = person.full_name_for_human if hasattr(person, "full_name_for_human") else str(person)

        title_with_prefix = f"{proposal.document_id} - {proposal.name or 'Untitled'}"
        add_header_footer(document, title_with_prefix, person_name, date_str)
        add_proposal_intro(document)
        add_proposal_section(document, proposal)
        add_links_section(document, proposal)

        updates = proposal.updates.all()
        add_updates_section(document, updates)
        add_attachments_section(document, proposal)

        safe_name = "".join(
            c if c.isalnum() or c in (" ", "-", "_") else "" for c in proposal.name or "proposal"
        )
        safe_name = safe_name.replace(" ", "_").lower()
        timestamp = now.strftime("%Y-%m-%d__%I:%M:%p").lower().replace(" ", "")
        filename = f"{proposal.document_id}_{safe_name}__{timestamp}.docx"

        file_stream = BytesIO()
        document.save(file_stream)
        file_stream.seek(0)

        response = HttpResponse(
            file_stream.read(),
            content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response

    except Exception:
        return generic_500(request=request)
