from typing import Mapping, Any
from django.http import HttpRequest, HttpResponse

from core.models.command import Command
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def command_detail_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        command = Command.objects.get(id=model_id)
    except Command.DoesNotExist:
        return generic_500(request=request)

    # Get historical records
    historical_records = command.history.all()

    context: Mapping[str, Any] = {
        'command': command,
        'historical_records': historical_records,
    }
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/command/command_detail.html'
    )
