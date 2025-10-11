from django.http import HttpRequest, HttpResponse

from core.models.report import Report
from core.views.generic.generic_view import generic_view


def report_view(request: HttpRequest) -> HttpResponse:
    return generic_view(
        model_cls=Report,
        name='report',
        request=request,
    )
