from django.http import HttpRequest, HttpResponse

from core.models.ai_governance import AIGovernance
from core.views.generic.generic_view import generic_view


def ai_governance_view(request: HttpRequest) -> HttpResponse:
    return generic_view(
        model_cls=AIGovernance,
        name='ai_governance',
        request=request,
    )
