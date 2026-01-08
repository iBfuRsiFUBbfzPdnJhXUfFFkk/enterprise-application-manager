from django.http import HttpRequest, HttpResponse

from core.models.hr_incident import HRIncident
from core.views.generic.generic_view import generic_view


def hr_incident_view(request: HttpRequest) -> HttpResponse:
    return generic_view(
        model_cls=HRIncident,
        name='hr_incident',
        request=request,
    )
