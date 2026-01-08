from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404

from core.models.hr_incident_update import HRIncidentUpdate


def hr_incident_download_update_attachment_view(request: HttpRequest, update_id: int) -> HttpResponse:
    update = get_object_or_404(HRIncidentUpdate, pk=update_id)

    if not update.attachment_blob_data:
        raise Http404("No attachment file for this update")

    response = HttpResponse(
        update.attachment_blob_data,
        content_type=update.attachment_blob_content_type or 'application/octet-stream'
    )
    response['Content-Disposition'] = f'attachment; filename="{update.attachment_blob_filename}"'
    return response
