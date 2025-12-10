from typing import Any, Mapping
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from core.forms.api_request_form import APIRequestForm
from core.models.api_request import APIRequest
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def api_request_edit_view(
    request: HttpRequest, model_id: int
) -> HttpResponse:
    try:
        api_request = APIRequest.objects.get(id=model_id)
    except APIRequest.DoesNotExist:
        return generic_500(request=request)

    if request.method == 'POST':
        form = APIRequestForm(request.POST, instance=api_request)
        if form.is_valid():
            form.save()
            return redirect(to='api_request')
    else:
        form = APIRequestForm(instance=api_request)

    context: Mapping[str, Any] = {'form': form}
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/api_request/api_request_form.html',
    )
