from django.http import HttpRequest, HttpResponse

from core.forms import DatabaseForm
from core.models.database import Database
from core.views.generic.generic_edit_view import generic_edit_view


def database_edit_view(request: HttpRequest, database_id: int) -> HttpResponse:
    return generic_edit_view(
        form_cls=DatabaseForm,
        model_cls=Database,
        model_id=database_id,
        request=request,
        success_route='database',
    )