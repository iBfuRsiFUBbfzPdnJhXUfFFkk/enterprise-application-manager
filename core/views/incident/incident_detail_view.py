from django.http import HttpRequest, HttpResponse

from core.models.incident import Incident
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def incident_detail_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        incident = Incident.objects.get(id=model_id)
        historical_records = incident.history.all()
    except Incident.DoesNotExist:
        return generic_500(request=request)

    return base_render(
        request=request,
        template_name='authenticated/incident/incident_detail.html',
        context={
            'incident': incident,
            'historical_records': historical_records,
        }
    )
