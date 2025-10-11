from django.http import HttpRequest, HttpResponse

from core.models.sprint import Sprint
from core.views.generic.generic_view import generic_view


def sprint_view(request: HttpRequest) -> HttpResponse:
    return generic_view(
        model_cls=Sprint,
        name='sprint',
        request=request,
    )
