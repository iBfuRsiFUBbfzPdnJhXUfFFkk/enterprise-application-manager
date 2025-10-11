from django.http import HttpRequest, HttpResponse

from core.models.application_group import ApplicationGroup
from core.views.generic.generic_delete_view import generic_delete_view


def application_group_delete_view(request: HttpRequest, model_id: int) -> HttpResponse:
    return generic_delete_view(
        model_cls=ApplicationGroup,
        model_id=model_id,
        request=request,
        success_route='application_group',
    )
