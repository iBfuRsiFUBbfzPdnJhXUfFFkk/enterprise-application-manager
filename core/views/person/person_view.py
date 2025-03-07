from django.http import HttpRequest, HttpResponse

from core.models.person import Person
from core.models.this_server_configuration import ThisServerConfiguration
from core.views.generic.generic_view import generic_view


def person_view(request: HttpRequest) -> HttpResponse:
    return generic_view(
        additional_context={
            'hostname_gitlab': ThisServerConfiguration.current().connection_git_lab_hostname
        },
        model_cls=Person,
        name='person',
        request=request,
    )
