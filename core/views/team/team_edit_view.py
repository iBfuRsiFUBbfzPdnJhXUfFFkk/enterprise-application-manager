from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.team_form import TeamForm
from core.models.team import Team
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def team_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        team = Team.objects.get(id=model_id)
    except Team.DoesNotExist:
        return generic_500(request=request)

    if request.method == 'POST':
        form = TeamForm(request.POST, instance=team)
        if form.is_valid():
            form.save()
            return redirect('team')
    else:
        form = TeamForm(instance=team)

    return base_render(
        request=request,
        template_name='authenticated/team/team_form.html',
        context={'form': form}
    )
