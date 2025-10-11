from django.http import HttpRequest, HttpResponse

from core.models.term import Term
from core.views.generic.generic_view import generic_view


def term_view(request: HttpRequest) -> HttpResponse:
    return generic_view(
        model_cls=Term,
        name='term',
        request=request,
    )
