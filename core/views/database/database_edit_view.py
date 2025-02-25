from django.http import HttpRequest, HttpResponse

from core.forms.database_form import DatabaseForm
from core.models.database import Database
from core.views.generic.generic_edit_view import generic_edit_view


def database_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    return generic_edit_view(
        decrypt_fields=['encrypted_password', 'encrypted_username'],
        form_cls=DatabaseForm,
        model_cls=Database,
        model_id=model_id,
        request=request,
        success_route='database',
    )
