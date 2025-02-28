from django.http import HttpRequest, HttpResponse

from core.models.secret import Secret
from core.views.generic.generic_view import generic_view


def secret_view(request: HttpRequest) -> HttpResponse:
    return generic_view(
        context_name="models",
        model_cls=Secret,
        request=request,
        template_name='secret/secret.html',
    )
