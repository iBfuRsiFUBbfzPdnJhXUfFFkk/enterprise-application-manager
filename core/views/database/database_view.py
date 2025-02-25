from django.http import HttpRequest, HttpResponse

from core.models.database import Database
from core.views.generic.generic_view import generic_view


def database_view(request: HttpRequest) -> HttpResponse:
    return generic_view(
        context_name="databases",
        field_names=['-id'],
        model_cls=Database,
        request=request,
        template_name='database.html',
    )