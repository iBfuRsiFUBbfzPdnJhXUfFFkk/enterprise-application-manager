from datetime import datetime, timezone
from io import BytesIO

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from docx import Document

from core.models.recommendation import Recommendation
from core.views.generic.generic_500 import generic_500
from core.views.recommendation.utilities.recommendation_docx_helpers import (
    add_header_footer,
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

        if not selected_ids:
            return generic_500(request=request)

        # Query with optimization
        recommendations = (
            Recommendation.objects.filter(id__in=selected_ids)
            .select_related(
                "application",
                "project",
                "estimation",
                "person_recommended_by",
            )
            .order_by("priority", "-date_recommended")
        )

        # Generate date string for header
        now = datetime.now(timezone.utc)
        date_str = now.strftime("%Y-%m-%d %I:%M %p UTC")

        # Create document
        document = Document()

        # Add each recommendation with its own section
        for i, recommendation in enumerate(recommendations):
            # Create new section for each recommendation (except the first)
            if i > 0:
                document.add_section()

            # Set margins for current section
            set_narrow_margins(document)

            # Get person who recommended (for header)
            person_name = ""
            if recommendation.person_recommended_by:
                person = recommendation.person_recommended_by
                person_name = person.full_name_for_human if hasattr(person, "full_name_for_human") else str(person)

            # Add header/footer for current section with recommendation-specific info
            add_header_footer(document, recommendation.name or "Untitled", person_name, date_str)

            # Add recommendation content
            add_recommendation_section(document, recommendation)

        # Generate filename
        now = datetime.now(timezone.utc)
        timestamp = now.strftime("%Y-%m-%d__%I:%M:%p").lower().replace(" ", "")
        filename = f"recommendations_export__{timestamp}.docx"

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
