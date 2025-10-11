from django.http import HttpRequest, HttpResponse

from core.models.requirement import Requirement
from core.views.generic.generic_view import generic_view


def requirement_view(request: HttpRequest) -> HttpResponse:
    return generic_view(
        model_cls=Requirement,
        name='requirement',
        request=request,
    )
