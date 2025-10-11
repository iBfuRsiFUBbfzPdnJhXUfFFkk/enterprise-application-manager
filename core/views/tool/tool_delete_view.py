from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.models.tool import Tool
from core.views.generic.generic_500 import generic_500


def tool_delete_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        tool = Tool.objects.get(id=model_id)
        tool.delete()
    except Tool.DoesNotExist:
        return generic_500(request=request)

    return redirect('tool')
