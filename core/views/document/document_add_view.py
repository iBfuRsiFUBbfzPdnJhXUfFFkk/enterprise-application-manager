from django.core.files.uploadedfile import UploadedFile
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.utils.datastructures import MultiValueDict

from core.forms.document_form import DocumentForm
from core.models.document import Document
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def document_add_view(request: HttpRequest) -> HttpResponse:
    immutable_query_dict = request.POST
    multi_value_dict_files: MultiValueDict[str, UploadedFile] = request.FILES
    method: str | None = request.method
    if method is None:
        return generic_500(request=request)
    if method == 'POST':
        form = DocumentForm(immutable_query_dict, multi_value_dict_files)
        is_valid: bool = form.is_valid()
        if is_valid:
            file: UploadedFile | None = form.cleaned_data['blob_data']
            if file is None:
                return generic_500(request=request)
            Document.objects.create(
                blob_content_type=file.content_type,
                blob_data=file.read(),
                blob_filename=file.name,
                blob_size=file.size,
                comment=immutable_query_dict['comment'],
                name=immutable_query_dict['name'],
                version=immutable_query_dict['version'],
            )
            return redirect(to='document')
    else:
        form = DocumentForm()

    return base_render(
        context={'form': form},
        request=request,
        template_name='common/generic_add_multipart.html',
    )
