from django.http import HttpRequest, HttpResponse

from core.models.external_blockers import ExternalBlockers
from core.views.generic.generic_view import generic_view


def external_blocker_view(request: HttpRequest) -> HttpResponse:
    return generic_view(
        model_cls=ExternalBlockers,
        name='external_blocker',
        request=request,
    )
