from django.db.models import Count
from django.http import HttpRequest, HttpResponse

from core.models.document import Document
from core.utilities.base_render import base_render


def document_view(request: HttpRequest) -> HttpResponse:
    """List all documents with pre-calculated counts to avoid N+1 queries."""
    documents = Document.objects.annotate(
        app_count=Count('applications', distinct=True),
        bad_int_count=Count('evidence_for_bad_interactions', distinct=True),
        bad_upd_count=Count('attachment_for_bad_interaction_updates', distinct=True),
        hr_upd_count=Count('attachment_for_hr_incident_updates', distinct=True),
    ).order_by('-uploaded_at')
    return base_render(
        context={'models': documents},
        request=request,
        template_name='authenticated/document/document.html',
    )
