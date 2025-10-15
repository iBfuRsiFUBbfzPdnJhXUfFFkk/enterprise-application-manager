from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.models.ai_hallucination import AIHallucination
from core.views.generic.generic_500 import generic_500


def ai_hallucination_delete_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        ai_hallucination = AIHallucination.objects.get(id=model_id)
        ai_hallucination.delete()
    except AIHallucination.DoesNotExist:
        return generic_500(request=request)

    return redirect('ai_hallucination')
