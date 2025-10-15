from django.http import HttpRequest, HttpResponse

from core.models.ai_use_case import AIUseCase
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def ai_use_case_detail_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        ai_use_case = AIUseCase.objects.get(id=model_id)
        historical_records = ai_use_case.history.all()
        hallucinations = ai_use_case.hallucinations.all()
    except AIUseCase.DoesNotExist:
        return generic_500(request=request)

    return base_render(
        request=request,
        template_name='authenticated/ai_use_case/ai_use_case_detail.html',
        context={
            'ai_use_case': ai_use_case,
            'historical_records': historical_records,
            'hallucinations': hallucinations,
        }
    )
