from django.http import HttpRequest, HttpResponse

from core.models.incident import Incident
from core.views.generic.generic_view import generic_view


def incident_view(request: HttpRequest) -> HttpResponse:
    return generic_view(
        additional_context={'incidents': Incident.objects.all()},
        model_cls=Incident,
        name='incident',
        request=request,
    )
