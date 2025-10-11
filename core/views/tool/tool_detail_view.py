from django.http import HttpRequest, HttpResponse

from core.models.tool import Tool
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def tool_detail_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        tool = Tool.objects.get(id=model_id)
        historical_records = tool.history.all()
    except Tool.DoesNotExist:
        return generic_500(request=request)

    return base_render(
        request=request,
        template_name='authenticated/tool/tool_detail.html',
        context={
            'tool': tool,
            'historical_records': historical_records,
        }
    )
