from django.http import HttpRequest, HttpResponse

from core.models.data_use_exception import DataUseException
from core.views.generic.generic_view import generic_view


def data_use_exception_view(request: HttpRequest) -> HttpResponse:
    return generic_view(
        model_cls=DataUseException,
        name='data_use_exception',
        request=request,
    )
