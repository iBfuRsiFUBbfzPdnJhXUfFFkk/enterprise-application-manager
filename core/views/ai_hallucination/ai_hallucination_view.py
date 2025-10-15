from django.http import HttpRequest, HttpResponse

from core.models.ai_hallucination import AIHallucination
from core.views.generic.generic_view import generic_view


def ai_hallucination_view(request: HttpRequest) -> HttpResponse:
    return generic_view(
        model_cls=AIHallucination,
        name='ai_hallucination',
        request=request,
    )
