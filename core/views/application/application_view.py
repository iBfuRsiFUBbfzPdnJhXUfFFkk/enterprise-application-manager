from django.http import HttpRequest, HttpResponse

from core.models.application import Application
from core.utilities.get_gitlab_hostname import get_gitlab_hostname
from core.views.generic.generic_view import generic_view


def application_view(request: HttpRequest) -> HttpResponse:
    return generic_view(
        context_name="applications",
        model_cls=Application,
        request=request,
        template_name='authenticated/application/application.html',
        additional_context={'hostname_gitlab': get_gitlab_hostname() or "gitlab.com"},
    )
