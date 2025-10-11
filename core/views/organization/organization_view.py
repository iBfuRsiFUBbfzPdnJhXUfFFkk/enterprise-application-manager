from django.http import HttpRequest, HttpResponse

from core.models.organization import Organization
from core.views.generic.generic_view import generic_view


def organization_view(request: HttpRequest) -> HttpResponse:
    return generic_view(
        model_cls=Organization,
        name='organization',
        request=request,
    )
