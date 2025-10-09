from typing import Mapping, Any

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.application_form import ApplicationForm
from core.models.application import Application
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def application_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        application = Application.objects.get(id=model_id)
    except Application.DoesNotExist:
        return generic_500(request=request)

    if request.method == 'POST':
        form = ApplicationForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            return redirect(to='application')
    else:
        form = ApplicationForm(instance=application)

    context: Mapping[str, Any] = {'form': form}
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/application/application_form.html'
    )
