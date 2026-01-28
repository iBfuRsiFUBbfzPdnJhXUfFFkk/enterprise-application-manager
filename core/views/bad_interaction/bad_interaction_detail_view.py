from typing import Any, Mapping

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404

from core.forms.bad_interaction_update_form import BadInteractionUpdateForm
from core.models.bad_interaction import BadInteraction
from core.utilities.base_render import base_render


def bad_interaction_detail_view(request: HttpRequest, model_id: int) -> HttpResponse:
    bad_interaction = get_object_or_404(
        BadInteraction.objects.select_related('person', 'reported_by', 'evidence_document').prefetch_related('hr_incidents', 'updates__created_by', 'updates__attachment_document'),
        pk=model_id
    )

    update_form = BadInteractionUpdateForm()

    context: Mapping[str, Any] = {
        'bad_interaction': bad_interaction,
        'update_form': update_form,
    }
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/bad_interaction/bad_interaction_detail.html'
    )
