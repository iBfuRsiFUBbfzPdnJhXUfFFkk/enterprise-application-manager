from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404

from core.models.bad_interaction import BadInteraction


def bad_interaction_download_evidence_view(request: HttpRequest, model_id: int) -> HttpResponse:
    bad_interaction = get_object_or_404(BadInteraction, pk=model_id)

    if not bad_interaction.evidence_blob_data:
        raise Http404("No evidence file attached to this interaction")

    response = HttpResponse(
        bad_interaction.evidence_blob_data,
        content_type=bad_interaction.evidence_blob_content_type or 'application/octet-stream'
    )
    response['Content-Disposition'] = f'attachment; filename="{bad_interaction.evidence_blob_filename}"'
    return response
