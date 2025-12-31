from datetime import datetime, timezone
from io import BytesIO

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from docx import Document

from core.models.it_devops_request import ITDevOpsRequest
from core.utilities.pdf_helpers import convert_docx_to_pdf
from core.views.generic.generic_500 import generic_500
from core.views.it_devops_request.utilities.it_devops_request_docx_helpers import (
    add_attachments_section,
    add_header_footer,
    add_links_section,
    add_request_intro,
    add_request_section,
    add_updates_section,
    set_narrow_margins,
)


@login_required
def it_devops_request_export_pdf_view(request: HttpRequest) -> HttpResponse:
    """Export IT/DevOps request to PDF with embedded attachments."""
    try:
        selected_ids = request.GET.get("ids", "").split(",")
        selected_ids = [int(id) for id in selected_ids if id.strip().isdigit()]

        if not selected_ids or len(selected_ids) != 1:
            return generic_500(request=request)

        try:
            it_devops_request = ITDevOpsRequest.objects.select_related(
                "application",
                "project",
                "person_requester",
                "person_assignee",
                "person_approver",
            ).prefetch_related(
                "attachments",
                "links",
                "updates__person_author",
            ).get(id=selected_ids[0])
        except ITDevOpsRequest.DoesNotExist:
            return generic_500(request=request)

        now = datetime.now(timezone.utc)
        date_str = now.strftime("%Y-%m-%d %I:%M %p UTC")

        document = Document()
        set_narrow_margins(document)

        person_name = ""
        if it_devops_request.person_requester:
            person = it_devops_request.person_requester
            person_name = person.full_name_for_human if hasattr(person, "full_name_for_human") else str(person)

        title_with_prefix = f"{it_devops_request.document_id} - {it_devops_request.name or 'Untitled'}"
        add_header_footer(document, title_with_prefix, person_name, date_str)
        add_request_intro(document)
        add_request_section(document, it_devops_request)
        add_links_section(document, it_devops_request)
        updates = it_devops_request.updates.all()
        add_updates_section(document, updates)

        # Add attachments section with embedded content (text, images, PDFs as images)
        add_attachments_section(document, it_devops_request)

        docx_stream = BytesIO()
        document.save(docx_stream)

        # Convert complete DOCX to PDF
        pdf_bytes = convert_docx_to_pdf(docx_stream.getvalue())
        if not pdf_bytes:
            # Fallback to DOCX if PDF conversion fails
            safe_name = "".join(
                c if c.isalnum() or c in (" ", "-", "_") else "" for c in it_devops_request.name or "request"
            )
            safe_name = safe_name.replace(" ", "_").lower()
            timestamp = now.strftime("%Y-%m-%d__%I:%M:%p").lower().replace(" ", "")
            filename = f"{it_devops_request.document_id}_{safe_name}__{timestamp}.docx"

            docx_stream.seek(0)
            response = HttpResponse(
                docx_stream.read(),
                content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
            response["Content-Disposition"] = f'attachment; filename="{filename}"'
            return response

        # Return PDF
        safe_name = "".join(
            c if c.isalnum() or c in (" ", "-", "_") else "" for c in it_devops_request.name or "request"
        )
        safe_name = safe_name.replace(" ", "_").lower()
        timestamp = now.strftime("%Y-%m-%d__%I:%M:%p").lower().replace(" ", "")
        filename = f"{it_devops_request.document_id}_{safe_name}__{timestamp}.pdf"

        response = HttpResponse(pdf_bytes, content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response

    except Exception:
        return generic_500(request=request)
