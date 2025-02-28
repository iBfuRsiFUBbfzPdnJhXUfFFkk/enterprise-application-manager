from django.http import HttpRequest, HttpResponse

from core.forms.secret_form import SecretForm
from core.views.generic.generic_add_view import generic_add_view


def secret_add_view(request: HttpRequest) -> HttpResponse:
    return generic_add_view(
        form_cls=SecretForm,
        request=request,
        success_route='secret',
    )
