from typing import Mapping, Any

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.procedure_step_form import ProcedureStepForm
from core.models.application import Application
from core.models.procedure_step import ProcedureStep
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


@login_required
def application_procedure_add_view(request: HttpRequest, model_id: int) -> HttpResponse:
    """Add a new procedure step to an application"""
    try:
        application = Application.objects.get(id=model_id)
    except Application.DoesNotExist:
        return generic_500(request=request)

    if request.method == 'POST':
        form = ProcedureStepForm(request.POST)
        if form.is_valid():
            step = form.save(commit=False)
            step.application = application

            # Set order to be after all existing steps
            max_order = ProcedureStep.objects.filter(application=application).count()
            step.order = (max_order + 1) * 10

            step.save()
            return redirect('application_procedure_list', model_id=model_id)
    else:
        form = ProcedureStepForm(initial={'application': application})

    context: Mapping[str, Any] = {
        'form': form,
        'application': application,
    }

    return base_render(
        context=context,
        request=request,
        template_name='authenticated/application/application_procedure_form.html'
    )
