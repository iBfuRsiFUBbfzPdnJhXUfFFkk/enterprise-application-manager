import uuid

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.models.document import Document


def document_rename_files_view(request: HttpRequest) -> HttpResponse:
    """Rename all document files to random UUIDs while preserving extensions."""
    if request.method != 'POST':
        return redirect('document')

    documents = Document.objects.filter(file__isnull=False).exclude(file='')
    renamed_count = 0

    for doc in documents:
        if doc.file:
            old_name = doc.file.name
            extension = ''
            if '.' in old_name:
                extension = '.' + old_name.rsplit('.', 1)[-1]

            new_filename = f"documents/{uuid.uuid4()}{extension}"

            # Rename the file in storage
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
