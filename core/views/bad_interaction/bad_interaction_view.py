from django.http import HttpRequest, HttpResponse

from core.models.bad_interaction import BadInteraction
from core.views.generic.generic_view import generic_view


def bad_interaction_view(request: HttpRequest) -> HttpResponse:
    return generic_view(
        model_cls=BadInteraction,
        name='bad_interaction',
        request=request,
    )
