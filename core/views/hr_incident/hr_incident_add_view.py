from typing import Any, Mapping

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.hr_incident_form import HRIncidentForm
from core.utilities.base_render import base_render


def hr_incident_add_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = HRIncidentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='hr_incident')
    else:
        form = HRIncidentForm()

    context: Mapping[str, Any] = {'form': form}
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/hr_incident/hr_incident_form.html'
    )
