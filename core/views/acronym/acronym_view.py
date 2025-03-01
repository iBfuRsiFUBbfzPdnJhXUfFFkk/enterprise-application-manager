from django.http import HttpRequest, HttpResponse

from core.models.acronym import Acronym
from core.views.generic.generic_view import generic_view


def acronym_view(request: HttpRequest) -> HttpResponse:
    return generic_view(
        model_cls=Acronym,
        name='acronym',
        request=request,
    )
