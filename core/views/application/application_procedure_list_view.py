from typing import Mapping, Any

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse

from core.models.application import Application
from core.models.procedure_step import ProcedureStep
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


@login_required
def application_procedure_list_view(request: HttpRequest, model_id: int) -> HttpResponse:
    """Display all procedure steps for an application with drag-and-drop reordering"""
    try:
        application = Application.objects.get(id=model_id)
    except Application.DoesNotExist:
        return generic_500(request=request)

    steps = ProcedureStep.objects.filter(application=application).order_by('order', 'id')

    context: Mapping[str, Any] = {
        'application': application,
        'steps': steps,
    }

    return base_render(
        context=context,
        request=request,
        template_name='authenticated/application/application_procedure_list.html'
    )
