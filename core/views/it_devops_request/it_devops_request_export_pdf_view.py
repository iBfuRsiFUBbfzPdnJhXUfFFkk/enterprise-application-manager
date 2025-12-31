from datetime import datetime, timezone
from io import BytesIO

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from docx import Document

from core.models.it_devops_request import ITDevOpsRequest
from core.utilities.pdf_helpers import (
    MAX_EMBED_SIZE,
    convert_docx_to_pdf,
    create_image_content_page,
    create_text_content_page,
    create_unsupported_file_page,
    get_attachment_handler,
    merge_pdfs,
)
from core.views.generic.generic_500 import generic_500
from core.views.it_devops_request.utilities.it_devops_request_docx_helpers import (
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

        docx_stream = BytesIO()
        document.save(docx_stream)

        pdf_bytes = convert_docx_to_pdf(docx_stream.getvalue())
        if not pdf_bytes:
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

        pdf_list = [pdf_bytes]

        for attachment in it_devops_request.attachments.all():
            if attachment.blob_size > MAX_EMBED_SIZE:
                page = create_unsupported_file_page(
                    attachment.blob_filename, attachment.blob_size, attachment.blob_content_type, "File too large (>10MB)"
                )
                pdf_list.append(page)
                continue

            handler = get_attachment_handler(attachment.blob_content_type)

            if handler == "text":
                try:
                    text = attachment.blob_data.decode("utf-8", errors="ignore")
                    page = create_text_content_page(text, attachment.blob_filename)
                    pdf_list.append(page)
                except Exception:
                    page = create_unsupported_file_page(
                        attachment.blob_filename, attachment.blob_size, attachment.blob_content_type, "Text decode error"
                    )
                    pdf_list.append(page)
            elif handler == "image":
                try:
                    page = create_image_content_page(attachment.blob_data, attachment.blob_filename)
                    pdf_list.append(page)
                except Exception:
                    page = create_unsupported_file_page(
                        attachment.blob_filename, attachment.blob_size, attachment.blob_content_type, "Image load error"
                    )
                    pdf_list.append(page)
            elif handler == "pdf":
                pdf_list.append(attachment.blob_data)
            else:
                page = create_unsupported_file_page(
                    attachment.blob_filename, attachment.blob_size, attachment.blob_content_type
                )
                pdf_list.append(page)

        final_pdf = merge_pdfs(pdf_list)

        safe_name = "".join(
            c if c.isalnum() or c in (" ", "-", "_") else "" for c in it_devops_request.name or "request"
        )
        safe_name = safe_name.replace(" ", "_").lower()
        timestamp = now.strftime("%Y-%m-%d__%I:%M:%p").lower().replace(" ", "")
        filename = f"{it_devops_request.document_id}_{safe_name}__{timestamp}.pdf"

        response = HttpResponse(final_pdf, content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response

    except Exception:
        return generic_500(request=request)
