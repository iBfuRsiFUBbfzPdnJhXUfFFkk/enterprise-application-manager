from django.http import HttpRequest, HttpResponse

from core.models.ai_governance import AIGovernance
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def ai_governance_detail_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        ai_governance = AIGovernance.objects.get(id=model_id)
        historical_records = ai_governance.history.all()
        use_cases = ai_governance.use_cases.all()
    except AIGovernance.DoesNotExist:
        return generic_500(request=request)

    return base_render(
        request=request,
        template_name='authenticated/ai_governance/ai_governance_detail.html',
        context={
            'ai_governance': ai_governance,
            'historical_records': historical_records,
            'use_cases': use_cases,
        }
    )
