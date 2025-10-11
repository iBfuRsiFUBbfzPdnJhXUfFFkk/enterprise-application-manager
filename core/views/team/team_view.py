from django.http import HttpRequest, HttpResponse

from core.models.team import Team
from core.views.generic.generic_view import generic_view


def team_view(request: HttpRequest) -> HttpResponse:
    return generic_view(
        model_cls=Team,
        name='team',
        request=request,
    )
