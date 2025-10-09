from typing import Mapping, Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.secret_form import SecretForm
from core.utilities.base_render import base_render


def secret_add_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = SecretForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='secret')
    else:
        form = SecretForm()

    context: Mapping[str, Any] = {'form': form}
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/secret/secret_form.html'
    )
