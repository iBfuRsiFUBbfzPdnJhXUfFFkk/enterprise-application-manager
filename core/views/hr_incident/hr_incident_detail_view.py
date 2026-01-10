from typing import Any, Mapping

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404

from core.forms.hr_incident_update_form import HRIncidentUpdateForm
from core.models.hr_incident import HRIncident
from core.utilities.base_render import base_render


def hr_incident_detail_view(request: HttpRequest, model_id: int) -> HttpResponse:
    hr_incident = get_object_or_404(
        HRIncident.objects.select_related('person', 'filed_by').prefetch_related('bad_interactions__person', 'updates__created_by', 'updates__documents'),
        pk=model_id
    )

    update_form = HRIncidentUpdateForm()

    context: Mapping[str, Any] = {
        'hr_incident': hr_incident,
        'update_form': update_form,
    }
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/hr_incident/hr_incident_detail.html'
    )
