from typing import Mapping, Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.document_form import DocumentForm
from core.utilities.base_render import base_render


def document_add_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            # Handle file upload
            if 'blob_data' in request.FILES:
                uploaded_file = request.FILES['blob_data']
                document.blob_data = uploaded_file.read()
                document.blob_filename = uploaded_file.name
                document.blob_size = uploaded_file.size
                document.blob_content_type = uploaded_file.content_type
            document.save()
            return redirect(to='document')
    else:
        form = DocumentForm()

    context: Mapping[str, Any] = {'form': form}
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/document/document_form.html'
    )
