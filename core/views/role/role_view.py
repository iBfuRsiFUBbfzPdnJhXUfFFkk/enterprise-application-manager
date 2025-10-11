from django.http import HttpRequest, HttpResponse

from core.models.role import Role
from core.views.generic.generic_view import generic_view


def role_view(request: HttpRequest) -> HttpResponse:
    return generic_view(
        model_cls=Role,
        name='role',
        request=request,
    )
