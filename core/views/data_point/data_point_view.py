from django.http import HttpRequest, HttpResponse

from core.models.data_point import DataPoint
from core.views.generic.generic_view import generic_view


def data_point_view(request: HttpRequest) -> HttpResponse:
    """
    List all data points.
    """
    return generic_view(
        model_cls=DataPoint,
        name='data_point',
        request=request,
    )
