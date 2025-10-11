from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.models.team import Team
from core.views.generic.generic_500 import generic_500


def team_delete_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        team = Team.objects.get(id=model_id)
        team.delete()
    except Team.DoesNotExist:
        return generic_500(request=request)

    return redirect('team')
