from typing import Any, Mapping

from django.http import HttpRequest, HttpResponse

from core.models.data_use_exception import DataUseException
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def data_use_exception_detail_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        data_use_exception = DataUseException.objects.get(id=model_id)
        historical_records = data_use_exception.history.all()
    except DataUseException.DoesNotExist:
        return generic_500(request, exception=Exception(f'DataUseException with id {model_id} does not exist'))

    context: Mapping[str, Any] = {
        'data_use_exception': data_use_exception,
        'historical_records': historical_records,
    }
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/data_use_exception/data_use_exception_detail.html'
    )
