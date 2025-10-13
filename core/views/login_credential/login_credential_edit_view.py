from typing import Mapping, Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.login_credential_form import LoginCredentialForm
from core.models.login_credential import LoginCredential
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def login_credential_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        login_credential = LoginCredential.objects.get(id=model_id)
    except LoginCredential.DoesNotExist:
        return generic_500(request=request)

    if request.method == 'POST':
        form = LoginCredentialForm(request.POST, instance=login_credential)
        if form.is_valid():
            form.save()
            return redirect(to='login_credential')
    else:
        form = LoginCredentialForm(instance=login_credential)

    context: Mapping[str, Any] = {
        'form': form,
        'decrypted_password': login_credential.get_decrypted_password(),
        'encrypted_password': login_credential.encrypted_password,
    }
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/login_credential/login_credential_form.html'
    )
