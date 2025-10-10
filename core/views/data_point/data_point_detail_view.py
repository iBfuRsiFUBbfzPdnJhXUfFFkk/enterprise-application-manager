from typing import Mapping, Any
from django.http import HttpRequest, HttpResponse

from core.models.data_point import DataPoint
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def data_point_detail_view(request: HttpRequest, model_id: int) -> HttpResponse:
    """
    Display data point details and change history.
    """
    try:
        data_point = DataPoint.objects.get(id=model_id)
        historical_records = data_point.history.all()
    except DataPoint.DoesNotExist:
        return generic_500(request, exception=Exception(f'DataPoint with id {model_id} does not exist'))

    context: Mapping[str, Any] = {
        'data_point': data_point,
        'historical_records': historical_records,
    }
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/data_point/data_point_detail.html'
    )
