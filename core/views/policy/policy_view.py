from django.http import HttpRequest, HttpResponse

from core.models.policy import Policy
from core.views.generic.generic_view import generic_view


def policy_view(request: HttpRequest) -> HttpResponse:
    return generic_view(
        model_cls=Policy,
        name='policy',
        request=request,
    )
