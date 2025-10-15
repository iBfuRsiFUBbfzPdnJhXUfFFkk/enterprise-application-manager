from django.http import HttpRequest, HttpResponse

from core.models.ai_hallucination import AIHallucination
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def ai_hallucination_detail_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        ai_hallucination = AIHallucination.objects.get(id=model_id)
        historical_records = ai_hallucination.history.all()
    except AIHallucination.DoesNotExist:
        return generic_500(request=request)

    return base_render(
        request=request,
        template_name='authenticated/ai_hallucination/ai_hallucination_detail.html',
        context={
            'ai_hallucination': ai_hallucination,
            'historical_records': historical_records,
        }
    )
