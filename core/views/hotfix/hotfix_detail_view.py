from typing import Any, Mapping

from django.http import HttpRequest, HttpResponse

from core.models.hotfix import Hotfix
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def hotfix_detail_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        hotfix = Hotfix.objects.get(id=model_id)
        historical_records = hotfix.history.all()
    except Hotfix.DoesNotExist:
        return generic_500(request, exception=Exception(f'Hotfix with id {model_id} does not exist'))

    context: Mapping[str, Any] = {
        'hotfix': hotfix,
        'historical_records': historical_records,
    }
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/hotfix/hotfix_detail.html'
    )
