from django.http import HttpRequest, HttpResponse

from core.models.application_group import ApplicationGroup
from core.views.generic.generic_view import generic_view


def application_group_view(request: HttpRequest) -> HttpResponse:
    return generic_view(
        context_name="application_groups",
        model_cls=ApplicationGroup,
        request=request,
        template_name='application_group.html',
    )
