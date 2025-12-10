from typing import Any, Mapping
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from core.forms.api_request_form import APIRequestForm
from core.utilities.base_render import base_render


def api_request_add_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = APIRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='api_request')
    else:
        form = APIRequestForm()

    context: Mapping[str, Any] = {'form': form}
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/api_request/api_request_form.html',
    )
