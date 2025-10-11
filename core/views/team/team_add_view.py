from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.team_form import TeamForm
from core.utilities.base_render import base_render


def team_add_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('team')
    else:
        form = TeamForm()

    return base_render(
        request=request,
        template_name='authenticated/team/team_form.html',
        context={'form': form}
    )
