from django.http import HttpRequest, HttpResponse

from core.models.acronym import Acronym
from core.views.generic.generic_view import generic_view


def acronym_view(request: HttpRequest) -> HttpResponse:
    return generic_view(
        context_name="acronyms",
        model_cls=Acronym,
        request=request,
        template_name='acronym.html',
    )
