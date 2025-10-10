from django.http import HttpRequest, HttpResponse

from core.models.hotfix import Hotfix
from core.views.generic.generic_view import generic_view


def hotfix_view(request: HttpRequest) -> HttpResponse:
    return generic_view(
        model_cls=Hotfix,
        name='hotfix',
        request=request,
    )
