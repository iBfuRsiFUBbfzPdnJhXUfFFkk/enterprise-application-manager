from django.core.files.uploadedfile import UploadedFile
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from core.forms.document_form import DocumentForm
from core.models.document import Document


def document_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    model_instance: Document = get_object_or_404(Document, id=model_id)
    if request.method == 'POST':
        immutable_query_dict: dict = request.POST
        form = DocumentForm(
            data=request.POST,
            files=request.FILES,
            instance=model_instance,
        )
        if form.is_valid():
            file: UploadedFile = form.cleaned_data['blob_data']
            model_instance.blob_content_type = file.content_type
            model_instance.blob_data = file.read()
            model_instance.blob_filename = file.name
            model_instance.blob_size = file.size
            model_instance.comment = immutable_query_dict['comment']
            model_instance.name = immutable_query_dict['name']
            model_instance.version = immutable_query_dict['version']
            model_instance.save()
            return redirect('document')
    else:
        form = DocumentForm(instance=model_instance)
    return render(
        request=request,
        template_name='generic_edit_multipart.html',
        context={'form': form}
    )
