from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.risk_form import RiskForm
from core.models.risk import Risk
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def risk_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        risk = Risk.objects.get(id=model_id)
    except Risk.DoesNotExist:
        return generic_500(request=request)

    if request.method == 'POST':
        form = RiskForm(request.POST, instance=risk)
        if form.is_valid():
            form.save()
            return redirect('risk')
    else:
        form = RiskForm(instance=risk)

    return base_render(
        request=request,
        template_name='authenticated/risk/risk_form.html',
        context={'form': form}
    )
