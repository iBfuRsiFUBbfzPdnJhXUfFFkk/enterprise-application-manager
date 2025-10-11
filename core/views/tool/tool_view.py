from django.http import HttpRequest, HttpResponse

from core.models.tool import Tool
from core.views.generic.generic_view import generic_view


def tool_view(request: HttpRequest) -> HttpResponse:
    return generic_view(
        model_cls=Tool,
        name='tool',
        request=request,
    )
