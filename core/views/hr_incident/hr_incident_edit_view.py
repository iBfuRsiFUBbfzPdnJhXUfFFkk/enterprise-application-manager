from typing import Any, Mapping

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect

from core.forms.hr_incident_form import HRIncidentForm
from core.models.hr_incident import HRIncident
from core.utilities.base_render import base_render


def hr_incident_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    hr_incident = get_object_or_404(HRIncident, pk=model_id)

    if request.method == 'POST':
        form = HRIncidentForm(request.POST, instance=hr_incident)
        if form.is_valid():
            form.save()
            return redirect(to='hr_incident')
    else:
        form = HRIncidentForm(instance=hr_incident)

    context: Mapping[str, Any] = {
        'form': form,
        'hr_incident': hr_incident,
    }
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/hr_incident/hr_incident_form.html'
    )
