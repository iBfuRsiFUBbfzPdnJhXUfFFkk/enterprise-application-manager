import hashlib

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.models.document import Document


def document_rehash_view(request: HttpRequest) -> HttpResponse:
    """Recalculate SHA-256 hashes for all documents."""
    if request.method != 'POST':
        return redirect('document')

    documents = Document.objects.filter(file__isnull=False).exclude(file='')
    updated = 0
    errors = 0

    for doc in documents:
        try:
            if doc.file:
                doc.file.seek(0)
                sha256 = hashlib.sha256()
                for chunk in doc.file.chunks():
                    sha256.update(chunk)
                doc.file_hash = sha256.hexdigest()
                doc.save(update_fields=['file_hash'])
                updated += 1
        except Exception:
            errors += 1

    if errors:
        messages.warning(request, f"Rehashed {updated} file(s) with {errors} error(s).")
    else:
        messages.success(request, f"Rehashed {updated} file(s).")

    return redirect('document')
