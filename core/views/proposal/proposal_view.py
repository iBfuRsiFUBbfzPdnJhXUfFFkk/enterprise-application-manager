from django.http import HttpRequest, HttpResponse

from core.models.proposal import Proposal
from core.views.generic.generic_view import generic_view


def proposal_view(request: HttpRequest) -> HttpResponse:
    return generic_view(
        model_cls=Proposal,
        name="proposal",
        request=request,
    )
