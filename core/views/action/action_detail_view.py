from typing import Mapping, Any
from django.http import HttpRequest, HttpResponse

from core.models.action import Action
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def action_detail_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        action = Action.objects.get(id=model_id)
    except Action.DoesNotExist:
        return generic_500(request=request)

    created_record = action.history.order_by('history_date').first()
    updated_record = action.history.order_by('-history_date').first()

    context: Mapping[str, Any] = {
        'model': action,
        'created_record': created_record,
        'updated_record': updated_record,
    }
    return base_render(context=context, request=request,
                      template_name='authenticated/action/action_detail.html')
