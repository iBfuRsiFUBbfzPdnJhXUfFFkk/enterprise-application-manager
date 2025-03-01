from django.http import HttpRequest, HttpResponse

from core.models.person import Person
from core.utilities.get_gitlab_hostname import get_gitlab_hostname
from core.views.generic.generic_view import generic_view


def person_view(request: HttpRequest) -> HttpResponse:
    return generic_view(
        context_name="people",
        model_cls=Person,
        request=request,
        template_name='person.html',
        additional_context={'hostname_gitlab': get_gitlab_hostname() or "gitlab.com"},
    )
