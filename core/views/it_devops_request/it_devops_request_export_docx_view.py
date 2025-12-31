from datetime import datetime, timezone
from io import BytesIO

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from docx import Document

from core.models.it_devops_request import ITDevOpsRequest
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
def it_devops_request_export_docx_view(request: HttpRequest) -> HttpResponse:
    """Export selected IT/DevOps request to DOCX document."""
    try:
        # Get selected IDs from query parameter
        selected_ids = request.GET.get("ids", "").split(",")
        selected_ids = [int(id) for id in selected_ids if id.strip().isdigit()]

        # Only allow exporting one request at a time
        if not selected_ids or len(selected_ids) != 1:
            return generic_500(request=request)

        # Get the single request
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

        # Generate date string for header
        now = datetime.now(timezone.utc)
        date_str = now.strftime("%Y-%m-%d %I:%M %p UTC")

        # Create document
        document = Document()
        set_narrow_margins(document)

        # Get requester name for header
        person_name = ""
        if it_devops_request.person_requester:
            person = it_devops_request.person_requester
            person_name = person.full_name_for_human if hasattr(person, "full_name_for_human") else str(person)

        # Add header/footer with request-specific info (prefixed with document ID)
        title_with_prefix = f"{it_devops_request.document_id} - {it_devops_request.name or 'Untitled'}"
        add_header_footer(document, title_with_prefix, person_name, date_str)

        # Add introductory paragraph
        add_request_intro(document)

        # Add request content
        add_request_section(document, it_devops_request)

        # Add links section
        add_links_section(document, it_devops_request)

        # Add updates timeline
        updates = it_devops_request.updates.all()
        add_updates_section(document, updates)

        # Add attachments section with embedded content
        add_attachments_section(document, it_devops_request)

        # Generate filename using document_id and request name
        safe_name = "".join(
            c if c.isalnum() or c in (" ", "-", "_") else "" for c in it_devops_request.name or "request"
        )
        safe_name = safe_name.replace(" ", "_").lower()
        timestamp = now.strftime("%Y-%m-%d__%I:%M:%p").lower().replace(" ", "")
        filename = f"{it_devops_request.document_id}_{safe_name}__{timestamp}.docx"

        # Save to BytesIO
        file_stream = BytesIO()
        document.save(file_stream)
        file_stream.seek(0)

        # Return response
        response = HttpResponse(
            file_stream.read(),
            content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response

    except Exception:
        return generic_500(request=request)
