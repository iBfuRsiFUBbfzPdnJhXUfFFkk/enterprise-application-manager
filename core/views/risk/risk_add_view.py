from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.risk_form import RiskForm
from core.utilities.base_render import base_render


def risk_add_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = RiskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('risk')
    else:
        form = RiskForm()

    return base_render(
        request=request,
        template_name='authenticated/risk/risk_form.html',
        context={'form': form}
    )
