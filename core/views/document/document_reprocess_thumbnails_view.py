import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods

from core.models.document import Document
from core.utilities.thumbnail_generator import generate_thumbnail

logger = logging.getLogger(__name__)


@login_required
@require_http_methods(["GET", "POST"])
def document_reprocess_thumbnails_view(request: HttpRequest) -> HttpResponse:
    """Regenerate thumbnails for all documents."""
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    documents = Document.objects.filter(file__isnull=False).exclude(file='')
    total = documents.count()

    # GET request returns just the count for the modal
    if request.method == 'GET' and is_ajax:
        return JsonResponse({'total': total})

    # POST processes the thumbnails
    if request.method != 'POST':
        return redirect('document')

    generated = 0
    skipped = 0
    errors = 0
    error_details = []

    for doc in documents:
        try:
            if doc.file:
                doc.file.seek(0)
                thumb = generate_thumbnail(doc.file, doc.file.name)
                if thumb:
                    doc.thumbnail = thumb
                    doc.save(update_fields=['thumbnail'])
                    generated += 1
                else:
                    skipped += 1
        except Exception as e:
            errors += 1
            error_msg = f"{doc.name or f'Document #{doc.pk}'}: {str(e)}"
            error_details.append(error_msg)
            logger.warning(f"Thumbnail generation failed: {error_msg}")

    if is_ajax:
        return JsonResponse({
            'success': True,
            'total': total,
            'generated': generated,
            'skipped': skipped,
            'errors': errors,
            'error_details': error_details[:10],
        })

    # Fallback for non-AJAX requests
    if errors:
        messages.warning(
            request,
            f"Generated {generated} thumbnail(s), {errors} error(s)."
        )
    else:
        messages.success(request, f"Generated {generated} thumbnail(s).")

    return redirect('document')
