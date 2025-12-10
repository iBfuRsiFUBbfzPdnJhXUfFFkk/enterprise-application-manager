from typing import Any, Mapping
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from core.forms.api_form import APIForm
from core.models.api import API
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def api_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        api = API.objects.get(id=model_id)
    except API.DoesNotExist:
        return generic_500(request=request)

    if request.method == 'POST':
        form = APIForm(request.POST, instance=api)
        if form.is_valid():
            form.save()
            return redirect(to='api')
    else:
        form = APIForm(instance=api)

    context: Mapping[str, Any] = {'form': form}
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/api/api_form.html',
    )
