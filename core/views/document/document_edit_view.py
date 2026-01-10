from typing import Mapping, Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.document_form import DocumentForm
from core.models.document import Document
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def document_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        document = Document.objects.get(id=model_id)
    except Document.DoesNotExist:
        return generic_500(request=request)

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()
            return redirect(to='document')
    else:
        form = DocumentForm(instance=document)

    context: Mapping[str, Any] = {'form': form}
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/document/document_form.html'
    )
