from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.incident_form import IncidentForm
from core.utilities.base_render import base_render


def incident_add_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = IncidentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('incident')
    else:
        form = IncidentForm()

    return base_render(
        request=request,
        template_name='authenticated/incident/incident_form.html',
        context={'form': form}
    )
