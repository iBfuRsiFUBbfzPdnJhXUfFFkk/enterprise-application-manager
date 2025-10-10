from typing import Mapping, Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.client_form import ClientForm
from core.models.client import Client
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def client_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    """
    Edit an existing client.
    """
    try:
        model = Client.objects.get(id=model_id)
    except Client.DoesNotExist:
        return generic_500(request, exception=Exception(f'Client with id {model_id} does not exist'))

    if request.method == 'POST':
        form = ClientForm(request.POST, instance=model)
        if form.is_valid():
            form.save()
            return redirect(to='client')
    else:
        form = ClientForm(instance=model)

    context: Mapping[str, Any] = {'form': form}
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/client/client_form.html'
    )
