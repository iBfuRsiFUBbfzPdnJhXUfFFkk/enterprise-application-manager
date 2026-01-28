import hashlib
import json
import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods

from core.models.document import Document
from core.utilities.image_similarity import compute_dhash, is_image_file

logger = logging.getLogger(__name__)


@login_required
@require_http_methods(["GET", "POST"])
def document_rehash_view(request: HttpRequest) -> HttpResponse:
    """Recalculate SHA-256 and image hashes for documents."""
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    # GET request returns list of document IDs for processing
    if request.method == 'GET' and is_ajax:
        doc_ids = list(
            Document.objects.filter(file__isnull=False)
            .exclude(file='')
            .values_list('id', flat=True)
        )
        return JsonResponse({'document_ids': doc_ids, 'total': len(doc_ids)})

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
                sha256 = hashlib.sha256()
                for chunk in doc.file.chunks():
                    sha256.update(chunk)
                doc.file_hash = sha256.hexdigest()

                # Compute image hash for image files
                is_image = is_image_file(doc.file.name)
                if is_image:
                    doc.file.seek(0)
                    doc.image_hash = compute_dhash(doc.file)
                else:
                    doc.image_hash = None

                doc.save(update_fields=['file_hash', 'image_hash'])

                return JsonResponse({
                    'success': True,
                    'status': 'hashed',
                    'name': doc_name,
                    'is_image': is_image and doc.image_hash is not None
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
            logger.warning(f"Rehash failed for doc {doc_id}: {error_msg}")
            return JsonResponse({
                'success': False,
                'status': 'error',
                'name': doc_name if 'doc_name' in dir() else f'Document #{doc_id}',
                'error': error_msg
            })

    # Non-AJAX fallback: batch process all documents
    documents = Document.objects.filter(file__isnull=False).exclude(file='')
    updated = 0
    images_hashed = 0
    errors = 0

    for doc in documents:
        try:
            if doc.file:
                doc.file.seek(0)
                sha256 = hashlib.sha256()
                for chunk in doc.file.chunks():
                    sha256.update(chunk)
                doc.file_hash = sha256.hexdigest()

                if is_image_file(doc.file.name):
                    doc.file.seek(0)
                    doc.image_hash = compute_dhash(doc.file)
                    if doc.image_hash:
                        images_hashed += 1
                else:
                    doc.image_hash = None

                doc.save(update_fields=['file_hash', 'image_hash'])
                updated += 1
        except Exception:
            errors += 1

    msg_parts = [f"Rehashed {updated} file(s)"]
    if images_hashed:
        msg_parts.append(f"{images_hashed} image(s)")
    if errors:
        msg_parts.append(f"{errors} error(s)")
        messages.warning(request, ", ".join(msg_parts) + ".")
    else:
        messages.success(request, ", ".join(msg_parts) + ".")

    return redirect('document')
