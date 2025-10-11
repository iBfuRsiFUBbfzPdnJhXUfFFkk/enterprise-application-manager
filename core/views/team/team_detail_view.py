from django.http import HttpRequest, HttpResponse

from core.models.team import Team
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def team_detail_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        team = Team.objects.get(id=model_id)
        historical_records = team.history.all()
    except Team.DoesNotExist:
        return generic_500(request=request)

    return base_render(
        request=request,
        template_name='authenticated/team/team_detail.html',
        context={
            'team': team,
            'historical_records': historical_records,
        }
    )
