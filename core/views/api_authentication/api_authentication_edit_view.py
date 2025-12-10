from typing import Any, Mapping
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from core.forms.api_authentication_form import APIAuthenticationForm
from core.models.api_authentication import APIAuthentication
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def api_authentication_edit_view(
    request: HttpRequest, model_id: int
) -> HttpResponse:
    try:
        auth = APIAuthentication.objects.get(id=model_id)
    except APIAuthentication.DoesNotExist:
        return generic_500(request=request)

    if request.method == 'POST':
        form = APIAuthenticationForm(request.POST, instance=auth)
        if form.is_valid():
            form.save()
            return redirect(to='api_detail', model_id=auth.api.id)
    else:
        form = APIAuthenticationForm(instance=auth)

    context: Mapping[str, Any] = {'form': form, 'api': auth.api}
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/api_authentication/api_authentication_form.html',
    )
