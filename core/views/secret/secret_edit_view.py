from django.http import HttpRequest, HttpResponse

from core.forms.secret_form import SecretForm
from core.models.secret import Secret
from core.views.generic.generic_edit_view import generic_edit_view


def secret_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    return generic_edit_view(
        decrypt_fields=['encrypted_value'],
        form_cls=SecretForm,
        model_cls=Secret,
        model_id=model_id,
        request=request,
        success_route='secret',
    )
