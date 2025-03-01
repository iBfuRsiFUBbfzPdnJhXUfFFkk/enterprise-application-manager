from django.http import HttpRequest, HttpResponse

from core.models.secret import Secret
from core.views.generic.generic_view import generic_view


def secret_view(request: HttpRequest) -> HttpResponse:
    return generic_view(
        model_cls=Secret,
        name='secret',
        request=request,
    )
