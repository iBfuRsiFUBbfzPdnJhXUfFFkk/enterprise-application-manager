from django.http import HttpRequest, HttpResponse

from core.models.recommendation import Recommendation
from core.views.generic.generic_view import generic_view


def recommendation_view(request: HttpRequest) -> HttpResponse:
    return generic_view(
        model_cls=Recommendation,
        name="recommendation",
        request=request,
    )
