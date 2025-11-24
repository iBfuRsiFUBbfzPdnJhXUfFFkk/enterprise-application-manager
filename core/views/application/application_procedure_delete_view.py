from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.models.procedure_step import ProcedureStep
from core.views.generic.generic_500 import generic_500


@login_required
def application_procedure_delete_view(request: HttpRequest, model_id: int, step_id: int) -> HttpResponse:
    """Delete a procedure step"""
    try:
        step = ProcedureStep.objects.get(id=step_id, application_id=model_id)
    except ProcedureStep.DoesNotExist:
        return generic_500(request=request)

    step.delete()
    return redirect('application_procedure_list', model_id=model_id)
