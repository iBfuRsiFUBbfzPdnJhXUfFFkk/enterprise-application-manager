from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.models.document import Document
from core.utilities.thumbnail_generator import generate_thumbnail


def document_reprocess_thumbnails_view(request: HttpRequest) -> HttpResponse:
    """Regenerate thumbnails for all documents."""
    if request.method != 'POST':
        return redirect('document')

    documents = Document.objects.filter(file__isnull=False).exclude(file='')
    generated = 0
    errors = 0

    for doc in documents:
        try:
            if doc.file:
                doc.file.seek(0)
                thumb = generate_thumbnail(doc.file, doc.file.name)
                if thumb:
                    doc.thumbnail = thumb
                    doc.save(update_fields=['thumbnail'])
                    generated += 1
        except Exception:
            errors += 1

    if errors:
        messages.warning(
            request,
            f"Generated {generated} thumbnail(s), {errors} error(s)."
        )
    else:
        messages.success(request, f"Generated {generated} thumbnail(s).")

    return redirect('document')
