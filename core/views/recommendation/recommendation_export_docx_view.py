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
    add_title_page,
    add_toc_placeholder,
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

        # Create document
        document = Document()
        set_narrow_margins(document)
        add_header_footer(document, "Recommendations Export")

        # Add title page
        username = request.user.get_full_name() or request.user.username
        add_title_page(document, username, recommendations.count())

        # Add TOC placeholder
        add_toc_placeholder(document)

        # Add each recommendation
        for i, recommendation in enumerate(recommendations):
            add_recommendation_section(document, recommendation)
            if i < recommendations.count() - 1:
                document.add_page_break()

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
