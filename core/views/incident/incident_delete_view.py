from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.models.incident import Incident
from core.views.generic.generic_500 import generic_500


def incident_delete_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        incident = Incident.objects.get(id=model_id)
        incident.delete()
    except Incident.DoesNotExist:
        return generic_500(request=request)

    return redirect('incident')
