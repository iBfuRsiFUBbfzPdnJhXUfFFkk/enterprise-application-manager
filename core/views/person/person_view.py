from os import getenv

from django.http import HttpRequest, HttpResponse

from core.models.person import Person
from core.views.generic.generic_view import generic_view


def person_view(request: HttpRequest) -> HttpResponse:
    return generic_view(
        context_name="people",
        model_cls=Person,
        request=request,
        template_name='person.html',
        additional_context={'hostname_gitlab': getenv('HOSTNAME_GITLAB') or "gitlab.com"},
    )
