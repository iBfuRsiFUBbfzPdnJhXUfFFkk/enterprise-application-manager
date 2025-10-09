from typing import Mapping, Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.application_group_form import ApplicationGroupForm
from core.models.application_group import ApplicationGroup
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def application_group_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        application_group = ApplicationGroup.objects.get(id=model_id)
    except ApplicationGroup.DoesNotExist:
        return generic_500(request=request)

    if request.method == 'POST':
        form = ApplicationGroupForm(request.POST, instance=application_group)
        if form.is_valid():
            form.save()
            return redirect(to='application_group')
    else:
        form = ApplicationGroupForm(instance=application_group)

    context: Mapping[str, Any] = {'form': form}
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/application_group/application_group_form.html'
    )
