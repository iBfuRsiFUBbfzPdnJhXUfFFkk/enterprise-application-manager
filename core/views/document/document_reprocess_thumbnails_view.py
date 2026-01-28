import json
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
    """Regenerate thumbnails for documents."""
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    # GET request returns list of document IDs for processing
    if request.method == 'GET' and is_ajax:
        doc_ids = list(
            Document.objects.filter(file__isnull=False)
            .exclude(file='')
            .values_list('id', flat=True)
        )
        return JsonResponse({'document_ids': doc_ids, 'total': len(doc_ids)})

    # POST processes a single document by ID (AJAX) or all documents (form)
    if request.method != 'POST':
        return redirect('document')

    # AJAX: Process single document
    if is_ajax:
        try:
            data = json.loads(request.body)
            doc_id = data.get('document_id')
        except (json.JSONDecodeError, KeyError):
            return JsonResponse({'error': 'Invalid request'}, status=400)

        try:
            doc = Document.objects.get(pk=doc_id)
            doc_name = doc.name or f'Document #{doc.pk}'

            if doc.file:
                doc.file.seek(0)
                thumb = generate_thumbnail(doc.file, doc.file.name)
                if thumb:
                    doc.thumbnail = thumb
                    doc.save(update_fields=['thumbnail'])
                    return JsonResponse({
                        'success': True,
                        'status': 'generated',
                        'name': doc_name
                    })
                else:
                    return JsonResponse({
                        'success': True,
                        'status': 'skipped',
                        'name': doc_name
                    })
        except Document.DoesNotExist:
            return JsonResponse({
                'success': False,
                'status': 'error',
                'name': f'Document #{doc_id}',
                'error': f'Document {doc_id} not found'
            })
        except Exception as e:
            error_msg = str(e)
            logger.warning(f"Thumbnail generation failed for doc {doc_id}: {error_msg}")
            return JsonResponse({
                'success': False,
                'status': 'error',
                'name': doc_name if 'doc_name' in dir() else f'Document #{doc_id}',
                'error': error_msg
            })

    # Non-AJAX fallback: batch process all documents
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
        messages.warning(request, f"Generated {generated} thumbnail(s), {errors} error(s).")
    else:
        messages.success(request, f"Generated {generated} thumbnail(s).")

    return redirect('document')
