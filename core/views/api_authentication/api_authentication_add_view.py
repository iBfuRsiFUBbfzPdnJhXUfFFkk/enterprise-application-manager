from typing import Any, Mapping
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from core.forms.api_authentication_form import APIAuthenticationForm
from core.models.api import API
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def api_authentication_add_view(
    request: HttpRequest, api_id: int
) -> HttpResponse:
    try:
        api = API.objects.get(id=api_id)
    except API.DoesNotExist:
        return generic_500(request=request)

    if request.method == 'POST':
        form = APIAuthenticationForm(request.POST)
        if form.is_valid():
            auth = form.save(commit=False)
            auth.api = api
            auth.save()
            return redirect(to='api_detail', model_id=api.id)
    else:
        form = APIAuthenticationForm(initial={'api': api})

    context: Mapping[str, Any] = {'form': form, 'api': api}
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/api_authentication/api_authentication_form.html',
    )
