from datetime import datetime, timezone
from io import BytesIO

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from docx import Document

from core.models.recommendation import Recommendation
from core.views.generic.generic_500 import generic_500
from core.views.recommendation.utilities.recommendation_docx_helpers import (
    add_header_footer,
    add_recommendation_intro,
    add_recommendation_section,
    set_narrow_margins,
)


@login_required
def recommendation_export_docx_view(request: HttpRequest) -> HttpResponse:
    """Export selected recommendations to DOCX document."""
    try:
        # Get selected IDs from query parameter
        selected_ids = request.GET.get("ids", "").split(",")
        selected_ids = [int(id) for id in selected_ids if id.strip().isdigit()]

        # Only allow exporting one recommendation at a time
        if not selected_ids or len(selected_ids) != 1:
            return generic_500(request=request)

        # Get the single recommendation
        try:
            recommendation = Recommendation.objects.select_related(
                "application",
                "project",
                "estimation",
                "person_recommended_by",
            ).prefetch_related("links").get(id=selected_ids[0])
        except Recommendation.DoesNotExist:
            return generic_500(request=request)

        # Generate date string for header
        now = datetime.now(timezone.utc)
        date_str = now.strftime("%Y-%m-%d %I:%M %p UTC")

        # Create document
        document = Document()
        set_narrow_margins(document)

        # Get person who recommended (for header)
        person_name = ""
        if recommendation.person_recommended_by:
            person = recommendation.person_recommended_by
            person_name = person.full_name_for_human if hasattr(person, "full_name_for_human") else str(person)

        # Add header/footer with recommendation-specific info (prefixed with "Recommendation - ")
        title_with_prefix = f"Recommendation - {recommendation.name or 'Untitled'}"
        add_header_footer(document, title_with_prefix, person_name, date_str)

        # Add introductory paragraph
        add_recommendation_intro(document)

        # Add recommendation content
        add_recommendation_section(document, recommendation)

        # Generate filename using recommendation name
        safe_name = "".join(c if c.isalnum() or c in (" ", "-", "_") else "" for c in recommendation.name or "recommendation")
        safe_name = safe_name.replace(" ", "_").lower()
        timestamp = now.strftime("%Y-%m-%d__%I:%M:%p").lower().replace(" ", "")
        filename = f"{safe_name}__{timestamp}.docx"

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
