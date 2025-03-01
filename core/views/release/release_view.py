from django.http import HttpRequest, HttpResponse

from core.models.release import Release
from core.views.generic.generic_view import generic_view


def release_view(request: HttpRequest) -> HttpResponse:
    return generic_view(
        model_cls=Release,
        name='release',
        request=request,
    )
