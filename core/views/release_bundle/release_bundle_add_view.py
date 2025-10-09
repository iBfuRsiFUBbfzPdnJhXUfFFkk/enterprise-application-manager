from typing import Mapping, Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.release_bundle_form import ReleaseBundleForm
from core.utilities.base_render import base_render


def release_bundle_add_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = ReleaseBundleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='release_bundle')
    else:
        form = ReleaseBundleForm()

    context: Mapping[str, Any] = {'form': form}
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/release_bundle/release_bundle_form.html'
    )
