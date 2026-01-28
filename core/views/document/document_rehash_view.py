import hashlib

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.models.document import Document
from core.utilities.image_similarity import compute_dhash, is_image_file


def document_rehash_view(request: HttpRequest) -> HttpResponse:
    """Recalculate SHA-256 and image hashes for all documents."""
    if request.method != 'POST':
        return redirect('document')

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

                # Compute image hash for image files
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
