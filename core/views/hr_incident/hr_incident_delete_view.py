from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect

from core.models.hr_incident import HRIncident


def hr_incident_delete_view(request: HttpRequest, model_id: int) -> HttpResponse:
    hr_incident = get_object_or_404(HRIncident, pk=model_id)
    hr_incident.delete()
    return redirect(to='hr_incident')
