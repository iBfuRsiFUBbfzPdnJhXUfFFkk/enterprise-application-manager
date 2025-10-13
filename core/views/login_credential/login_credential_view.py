from django.http import HttpRequest, HttpResponse

from core.models.login_credential import LoginCredential
from core.views.generic.generic_view import generic_view


def login_credential_view(request: HttpRequest) -> HttpResponse:
    return generic_view(
        model_cls=LoginCredential,
        name='login_credential',
        request=request,
    )
