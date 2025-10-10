from typing import Mapping, Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.client_form import ClientForm
from core.utilities.base_render import base_render


def client_add_view(request: HttpRequest) -> HttpResponse:
    """
    Create a new client.
    """
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='client')
    else:
        form = ClientForm()

    context: Mapping[str, Any] = {'form': form}
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/client/client_form.html'
    )
