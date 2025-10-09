from typing import Mapping, Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.release_bundle_form import ReleaseBundleForm
from core.models.release_bundle import ReleaseBundle
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def release_bundle_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        release_bundle = ReleaseBundle.objects.get(id=model_id)
    except ReleaseBundle.DoesNotExist:
        return generic_500(request=request)

    if request.method == 'POST':
        form = ReleaseBundleForm(request.POST, instance=release_bundle)
        if form.is_valid():
            form.save()
            return redirect(to='release_bundle')
    else:
        form = ReleaseBundleForm(instance=release_bundle)

    context: Mapping[str, Any] = {'form': form}
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/release_bundle/release_bundle_form.html'
    )
