from typing import Any, Mapping

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.external_blocker_form import ExternalBlockerForm
from core.models.external_blockers import ExternalBlockers
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def external_blocker_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        external_blocker = ExternalBlockers.objects.get(id=model_id)
    except ExternalBlockers.DoesNotExist:
        return generic_500(request, exception=Exception(f'ExternalBlockers with id {model_id} does not exist'))

    if request.method == 'POST':
        form = ExternalBlockerForm(request.POST, instance=external_blocker)
        if form.is_valid():
            form.save()
            return redirect(to='external_blocker')
    else:
        form = ExternalBlockerForm(instance=external_blocker)

    context: Mapping[str, Any] = {'form': form}
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/external_blocker/external_blocker_form.html'
    )
