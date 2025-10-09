from typing import Mapping, Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.release_form import ReleaseForm
from core.utilities.base_render import base_render


def release_add_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = ReleaseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='release')
    else:
        form = ReleaseForm()

    context: Mapping[str, Any] = {'form': form}
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/release/release_form.html'
    )
