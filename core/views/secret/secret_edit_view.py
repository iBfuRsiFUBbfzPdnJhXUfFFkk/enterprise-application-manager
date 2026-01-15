from typing import Mapping, Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.secret_form import SecretForm
from core.models.secret import Secret
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def secret_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        secret = Secret.objects.get(id=model_id)
    except Secret.DoesNotExist:
        return generic_500(request=request)

    if request.method == 'POST':
        form = SecretForm(request.POST, instance=secret)
        if form.is_valid():
            form.save()
            return redirect(to='secret_detail', model_id=secret.id)
    else:
        form = SecretForm(instance=secret)

    context: Mapping[str, Any] = {
        'form': form,
    }
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/secret/secret_form.html'
    )
