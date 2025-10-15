from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.ai_governance_form import AIGovernanceForm
from core.utilities.base_render import base_render


def ai_governance_add_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = AIGovernanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ai_governance')
    else:
        form = AIGovernanceForm()

    return base_render(
        request=request,
        template_name='authenticated/ai_governance/ai_governance_form.html',
        context={'form': form}
    )
