from django.http import HttpRequest, HttpResponse

from core.models.action import Action
from core.views.generic.generic_view import generic_view


def action_view(request: HttpRequest) -> HttpResponse:
    return generic_view(
        model_cls=Action,
        name='action',
        request=request,
    )
