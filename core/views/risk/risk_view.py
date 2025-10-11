from django.http import HttpRequest, HttpResponse

from core.models.risk import Risk
from core.views.generic.generic_view import generic_view


def risk_view(request: HttpRequest) -> HttpResponse:
    return generic_view(
        model_cls=Risk,
        name='risk',
        request=request,
    )
