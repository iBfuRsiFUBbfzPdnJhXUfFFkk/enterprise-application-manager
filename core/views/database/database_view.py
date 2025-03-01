from django.http import HttpRequest, HttpResponse

from core.models.database import Database
from core.views.generic.generic_view import generic_view


def database_view(request: HttpRequest) -> HttpResponse:
    return generic_view(
        model_cls=Database,
        name='database',
        request=request,
    )
