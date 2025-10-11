from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.onboard_procedure_form import OnboardProcedureForm
from core.utilities.base_render import base_render


def onboard_procedure_add_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = OnboardProcedureForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('onboard_procedure')
    else:
        form = OnboardProcedureForm()

    return base_render(
        request=request,
        template_name='authenticated/onboard_procedure/onboard_procedure_form.html',
        context={'form': form}
    )
