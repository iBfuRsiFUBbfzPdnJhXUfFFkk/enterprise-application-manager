from django.http import HttpRequest, HttpResponse

from core.models.ai_use_case import AIUseCase
from core.views.generic.generic_view import generic_view


def ai_use_case_view(request: HttpRequest) -> HttpResponse:
    return generic_view(
        model_cls=AIUseCase,
        name='ai_use_case',
        request=request,
    )
