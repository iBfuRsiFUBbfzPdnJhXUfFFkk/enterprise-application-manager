import json
import logging
import uuid

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods

from core.models.document import Document

logger = logging.getLogger(__name__)


@login_required
@require_http_methods(["GET", "POST"])
def document_rename_files_view(request: HttpRequest) -> HttpResponse:
    """Rename document files to random UUIDs while preserving extensions."""
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
                old_name = doc.file.name
                extension = ''
                if '.' in old_name:
                    extension = '.' + old_name.rsplit('.', 1)[-1]

                new_filename = f"documents/{uuid.uuid4()}{extension}"

                storage = doc.file.storage
                if storage.exists(old_name):
                    old_file = storage.open(old_name, 'rb')
                    storage.save(new_filename, old_file)
                    old_file.close()
                    storage.delete(old_name)

                    doc.file.name = new_filename
                    doc.save()

                    return JsonResponse({
                        'success': True,
                        'status': 'renamed',
                        'name': doc_name
                    })
                else:
                    return JsonResponse({
                        'success': True,
                        'status': 'skipped',
                        'name': doc_name,
                        'reason': 'File not found in storage'
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
            logger.warning(f"Rename failed for doc {doc_id}: {error_msg}")
            return JsonResponse({
                'success': False,
                'status': 'error',
                'name': doc_name if 'doc_name' in dir() else f'Document #{doc_id}',
                'error': error_msg
            })

    # Non-AJAX fallback: batch process all documents
    documents = Document.objects.filter(file__isnull=False).exclude(file='')
    renamed_count = 0

    for doc in documents:
        if doc.file:
            old_name = doc.file.name
            extension = ''
            if '.' in old_name:
                extension = '.' + old_name.rsplit('.', 1)[-1]

            new_filename = f"documents/{uuid.uuid4()}{extension}"

            storage = doc.file.storage
            if storage.exists(old_name):
                old_file = storage.open(old_name, 'rb')
                storage.save(new_filename, old_file)
                old_file.close()
                storage.delete(old_name)

                doc.file.name = new_filename
                doc.save()
                renamed_count += 1

    messages.success(request, f"Renamed {renamed_count} file(s) to random UUIDs.")
    return redirect('document')
