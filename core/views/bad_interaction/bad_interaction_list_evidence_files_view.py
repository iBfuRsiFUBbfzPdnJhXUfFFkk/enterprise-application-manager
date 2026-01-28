from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from core.models.document import Document


@login_required
def bad_interaction_list_evidence_files_view(request):
    """List all documents with files for selection as evidence."""
    files = []

    # Get all documents that have files
    documents = Document.objects.exclude(file='').exclude(file__isnull=True)

    for doc in documents:
        try:
            # Check if file actually exists
            if not doc.file.storage.exists(doc.file.name):
                continue

            file_url = doc.get_file_url()
            file_size = doc.get_file_size()
            filename = doc.get_filename() or doc.name

            # Determine file type for preview
            lower_name = filename.lower() if filename else ''
            if lower_name.endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp', '.svg')):
                file_type = 'image'
            elif lower_name.endswith('.pdf'):
                file_type = 'pdf'
            else:
                file_type = 'other'

            files.append({
                'id': doc.id,
                'name': str(doc),
                'filename': filename,
                'url': file_url,
                'size': file_size or 0,
                'type': file_type,
            })
        except Exception:
            continue

    # Sort by name
    files.sort(key=lambda x: x['name'])

    return JsonResponse({'files': files})
