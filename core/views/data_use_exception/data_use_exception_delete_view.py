from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.models.data_use_exception import DataUseException
from core.views.generic.generic_500 import generic_500


def data_use_exception_delete_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        data_use_exception = DataUseException.objects.get(id=model_id)
        data_use_exception.delete()
    except DataUseException.DoesNotExist:
        return generic_500(request=request)

    return redirect(to='data_use_exception')
