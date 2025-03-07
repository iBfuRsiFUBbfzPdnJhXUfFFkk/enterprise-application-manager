from django.http import HttpRequest, HttpResponse

from core.models.application import Application
from core.models.this_server_configuration import ThisServerConfiguration
from core.views.generic.generic_view import generic_view


def application_view(request: HttpRequest) -> HttpResponse:
    return generic_view(
        additional_context={
            'hostname_gitlab': ThisServerConfiguration.current().connection_git_lab_hostname
        },
        model_cls=Application,
        name='application',
        request=request,
    )
