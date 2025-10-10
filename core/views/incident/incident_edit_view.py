from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.incident_form import IncidentForm
from core.models.incident import Incident
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def incident_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        incident = Incident.objects.get(id=model_id)
    except Incident.DoesNotExist:
        return generic_500(request=request)

    if request.method == 'POST':
        form = IncidentForm(request.POST, instance=incident)
        if form.is_valid():
            form.save()
            return redirect('incident')
    else:
        form = IncidentForm(instance=incident)

    return base_render(
        request=request,
        template_name='authenticated/incident/incident_form.html',
        context={'form': form}
    )
