from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, get_object_or_404

from core.models.bad_interaction import BadInteraction
from core.models.bad_interaction_update import BadInteractionUpdate
from core.models.document import Document
from core.models.hr_incident_update import HRIncidentUpdate


def document_merge_duplicates_view(request: HttpRequest) -> HttpResponse:
    """Merge selected duplicate documents into the kept one."""
    if request.method != 'POST':
        return redirect('document_duplicates')

    keep_id = request.POST.get('keep_id')
    delete_ids = request.POST.getlist('delete_ids')

    if not keep_id:
        messages.error(request, "Please select a document to keep.")
        return redirect('document_duplicates')

    if not delete_ids:
        messages.error(request, "Please select at least one document to delete.")
        return redirect('document_duplicates')

    keep_doc = get_object_or_404(Document, pk=keep_id)

    merged_count = 0
    for delete_id in delete_ids:
        if delete_id == keep_id:
            continue

        try:
            dup = Document.objects.get(pk=delete_id)

            # Move BadInteraction references
            BadInteraction.objects.filter(evidence_document=dup).update(evidence_document=keep_doc)

            # Move BadInteractionUpdate references
            BadInteractionUpdate.objects.filter(attachment_document=dup).update(attachment_document=keep_doc)

            # Move HRIncidentUpdate references
            HRIncidentUpdate.objects.filter(attachment_document=dup).update(attachment_document=keep_doc)

            # Move Application M2M references
            for app in dup.applications.all():
                if not keep_doc.applications.filter(pk=app.pk).exists():
                    keep_doc.applications.add(app)

            # Delete the duplicate document
            dup.delete()
            merged_count += 1

        except Document.DoesNotExist:
            continue

    if merged_count:
        messages.success(request, f"Deleted {merged_count} duplicate(s), moved all relations to '{keep_doc.name}'.")
    else:
        messages.warning(request, "No documents were merged.")

    return redirect('document_duplicates')
