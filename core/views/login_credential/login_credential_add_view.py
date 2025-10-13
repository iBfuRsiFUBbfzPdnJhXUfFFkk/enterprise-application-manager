from typing import Mapping, Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.login_credential_form import LoginCredentialForm
from core.utilities.base_render import base_render


def login_credential_add_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = LoginCredentialForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='login_credential')
    else:
        form = LoginCredentialForm()

    context: Mapping[str, Any] = {'form': form}
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/login_credential/login_credential_form.html'
    )
