from django.http import HttpRequest, HttpResponse

from core.models.approval import Approval
from core.views.generic.generic_view import generic_view


def approval_view(request: HttpRequest) -> HttpResponse:
    return generic_view(
        model_cls=Approval,
        name="approval",
        request=request,
    )
