from django.http import HttpRequest, HttpResponse

from core.models.it_devops_request import ITDevOpsRequest
from core.views.generic.generic_view import generic_view


def it_devops_request_view(request: HttpRequest) -> HttpResponse:
    return generic_view(
        model_cls=ITDevOpsRequest,
        name="it_devops_request",
        request=request,
    )
