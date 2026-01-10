from typing import Mapping, Any
from django.http import HttpRequest, HttpResponse
import mimetypes

from core.models.document import Document
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def document_detail_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        document = Document.objects.get(id=model_id)
    except Document.DoesNotExist:
        return generic_500(request=request)

    # Get history records for created/updated tracking
    created_record = document.history.order_by('history_date').first()
    updated_record = document.history.order_by('-history_date').first()

    # Determine file type for preview routing
    file_type = None
    mime_type = None

    if document.has_file:
        filename = document.get_filename()
        mime_type = document.blob_content_type if document.blob_content_type else None

        if not mime_type and filename:
            mime_type, _ = mimetypes.guess_type(filename)

        # Categorize for template
        if mime_type:
            if mime_type.startswith('image/'):
                file_type = 'image'
            elif mime_type == 'application/pdf':
                file_type = 'pdf'
            elif mime_type.startswith('text/') or mime_type in [
                'application/json', 'application/xml', 'text/csv', 'text/markdown'
            ]:
                file_type = 'text'
            else:
                file_type = 'other'

    # Prefetch M2M relationships
    applications = document.applications.all()
    bad_interactions = document.bad_interactions.all()
    bad_interaction_updates = document.bad_interaction_updates.all()
    hr_incident_updates = document.hr_incident_updates.all()

    context: Mapping[str, Any] = {
        'model': document,
        'created_record': created_record,
        'updated_record': updated_record,
        'file_type': file_type,
        'mime_type': mime_type,
        'applications': applications,
        'bad_interactions': bad_interactions,
        'bad_interaction_updates': bad_interaction_updates,
        'hr_incident_updates': hr_incident_updates,
    }

    return base_render(
        context=context,
        request=request,
        template_name='authenticated/document/document_detail.html'
    )
