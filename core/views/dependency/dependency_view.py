from django.http import HttpRequest, HttpResponse

from core.models.dependency import Dependency
from core.views.generic.generic_view import generic_view


def dependency_view(request: HttpRequest) -> HttpResponse:
    return generic_view(
        context_name="dependencies",
        model_cls=Dependency,
        request=request,
        template_name='dependency.html',
    )
