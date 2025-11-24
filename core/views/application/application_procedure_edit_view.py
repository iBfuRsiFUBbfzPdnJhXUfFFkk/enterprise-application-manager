from typing import Mapping, Any

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.procedure_step_form import ProcedureStepForm
from core.models.procedure_step import ProcedureStep
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


@login_required
def application_procedure_edit_view(request: HttpRequest, model_id: int, step_id: int) -> HttpResponse:
    """Edit an existing procedure step"""
    try:
        step = ProcedureStep.objects.get(id=step_id, application_id=model_id)
    except ProcedureStep.DoesNotExist:
        return generic_500(request=request)

    application = step.application

    if request.method == 'POST':
        form = ProcedureStepForm(request.POST, instance=step)
        if form.is_valid():
            form.save()
            return redirect('application_procedure_list', model_id=model_id)
    else:
        form = ProcedureStepForm(instance=step)

    context: Mapping[str, Any] = {
        'form': form,
        'application': application,
        'step': step,
    }

    return base_render(
        context=context,
        request=request,
        template_name='authenticated/application/application_procedure_form.html'
    )
