from typing import Any, Mapping

from django.http import HttpRequest, HttpResponse

from core.models.external_blockers import ExternalBlockers
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def external_blocker_detail_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        external_blocker = ExternalBlockers.objects.get(id=model_id)
        historical_records = external_blocker.history.all()
    except ExternalBlockers.DoesNotExist:
        return generic_500(request, exception=Exception(f'ExternalBlockers with id {model_id} does not exist'))

    context: Mapping[str, Any] = {
        'external_blocker': external_blocker,
        'historical_records': historical_records,
    }
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/external_blocker/external_blocker_detail.html'
    )
