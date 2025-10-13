from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.models.login_credential import LoginCredential
from core.views.generic.generic_500 import generic_500


def login_credential_delete_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        login_credential = LoginCredential.objects.get(id=model_id)
        login_credential.delete()
    except LoginCredential.DoesNotExist:
        return generic_500(request=request)

    return redirect('login_credential')
