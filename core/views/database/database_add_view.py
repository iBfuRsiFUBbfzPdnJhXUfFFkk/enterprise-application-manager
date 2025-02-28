from django.http import HttpRequest, HttpResponse

from core.forms.database_form import DatabaseForm
from core.views.generic.generic_add_view import generic_add_view


def database_add_view(request: HttpRequest) -> HttpResponse:
    return generic_add_view(
        form_cls=DatabaseForm,
        request=request,
        success_route='database',
    )
