from django.http import HttpRequest, HttpResponse

from core.models.formula import Formula
from core.views.generic.generic_view import generic_view


def formula_view(request: HttpRequest) -> HttpResponse:
    return generic_view(
        model_cls=Formula,
        name='formula',
        request=request,
    )
