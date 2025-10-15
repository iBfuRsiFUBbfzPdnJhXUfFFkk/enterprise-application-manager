from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.ai_governance_form import AIGovernanceForm
from core.models.ai_governance import AIGovernance
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def ai_governance_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        ai_governance = AIGovernance.objects.get(id=model_id)
    except AIGovernance.DoesNotExist:
        return generic_500(request=request)

    if request.method == 'POST':
        form = AIGovernanceForm(request.POST, instance=ai_governance)
        if form.is_valid():
            form.save()
            return redirect('ai_governance')
    else:
        form = AIGovernanceForm(instance=ai_governance)

    return base_render(
        request=request,
        template_name='authenticated/ai_governance/ai_governance_form.html',
        context={'form': form}
    )
