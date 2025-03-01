from django.http import HttpRequest, HttpResponse

from core.models.person import Person
from core.utilities.get_gitlab_hostname import get_gitlab_hostname
from core.views.generic.generic_view import generic_view


def person_view(request: HttpRequest) -> HttpResponse:
    return generic_view(
        additional_context={'hostname_gitlab': get_gitlab_hostname() or "gitlab.com"},
        model_cls=Person,
        name='person',
        request=request,
    )
