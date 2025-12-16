from django.http import HttpRequest, HttpResponse

from core.models.competitor import Competitor
from core.views.generic.generic_view import generic_view


def competitor_view(request: HttpRequest) -> HttpResponse:
    return generic_view(
        model_cls=Competitor,
        name='competitor',
        request=request,
    )
