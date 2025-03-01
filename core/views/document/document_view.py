from django.http import HttpRequest, HttpResponse

from core.models.document import Document
from core.views.generic.generic_view import generic_view


def document_view(request: HttpRequest) -> HttpResponse:
    return generic_view(
        model_cls=Document,
        name='document',
        request=request,
    )
