from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.models.ai_governance import AIGovernance
from core.views.generic.generic_500 import generic_500


def ai_governance_delete_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        ai_governance = AIGovernance.objects.get(id=model_id)
        ai_governance.delete()
    except AIGovernance.DoesNotExist:
        return generic_500(request=request)

    return redirect('ai_governance')
