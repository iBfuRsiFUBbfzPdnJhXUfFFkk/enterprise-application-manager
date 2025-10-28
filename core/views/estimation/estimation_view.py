from django.http import HttpRequest, HttpResponse

from core.models.estimation import Estimation
from core.views.generic.generic_view import generic_view


def estimation_view(request: HttpRequest) -> HttpResponse:
    return generic_view(
        model_cls=Estimation,
        name='estimation',
        request=request,
    )
