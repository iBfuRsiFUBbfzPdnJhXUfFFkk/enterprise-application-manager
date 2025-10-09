from typing import Mapping, Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.release_form import ReleaseForm
from core.models.release import Release
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def release_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        release = Release.objects.get(id=model_id)
    except Release.DoesNotExist:
        return generic_500(request=request)

    if request.method == 'POST':
        form = ReleaseForm(request.POST, instance=release)
        if form.is_valid():
            form.save()
            return redirect(to='release')
    else:
        form = ReleaseForm(instance=release)

    context: Mapping[str, Any] = {'form': form}
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/release/release_form.html'
    )
