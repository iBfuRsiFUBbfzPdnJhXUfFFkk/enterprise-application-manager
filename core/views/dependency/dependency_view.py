from django.http import HttpRequest, HttpResponse

from core.models.dependency import Dependency
from core.views.generic.generic_view import generic_view


def dependency_view(request: HttpRequest) -> HttpResponse:
    return generic_view(
        model_cls=Dependency,
        name='dependency',
        request=request,
    )
