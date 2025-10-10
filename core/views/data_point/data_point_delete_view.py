from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.models.data_point import DataPoint
from core.views.generic.generic_500 import generic_500


def data_point_delete_view(request: HttpRequest, model_id: int) -> HttpResponse:
    """
    Delete a data point.
    """
    try:
        data_point = DataPoint.objects.get(id=model_id)
        data_point.delete()
    except DataPoint.DoesNotExist:
        return generic_500(request=request)

    return redirect(to='data_point')
