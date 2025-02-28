from os import getenv

from django.http import HttpRequest, HttpResponse

from core.models.application import Application
from core.views.generic.generic_view import generic_view


def application_view(request: HttpRequest) -> HttpResponse:
    return generic_view(
        context_name="applications",
        model_cls=Application,
        request=request,
        template_name='application.html',
        additional_context={'hostname_gitlab': getenv('HOSTNAME_GITLAB') or "gitlab.com"},
    )
