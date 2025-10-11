from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.onboard_procedure_form import OnboardProcedureForm
from core.models.onboard_procedure import OnboardProcedure
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def onboard_procedure_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        onboard_procedure = OnboardProcedure.objects.get(id=model_id)
    except OnboardProcedure.DoesNotExist:
        return generic_500(request=request)

    if request.method == 'POST':
        form = OnboardProcedureForm(request.POST, instance=onboard_procedure)
        if form.is_valid():
            form.save()
            return redirect('onboard_procedure')
    else:
        form = OnboardProcedureForm(instance=onboard_procedure)

    return base_render(
        request=request,
        template_name='authenticated/onboard_procedure/onboard_procedure_form.html',
        context={'form': form}
    )
