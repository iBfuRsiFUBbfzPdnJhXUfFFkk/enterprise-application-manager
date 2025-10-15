from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.models.ai_use_case import AIUseCase
from core.views.generic.generic_500 import generic_500


def ai_use_case_delete_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        ai_use_case = AIUseCase.objects.get(id=model_id)
        ai_use_case.delete()
    except AIUseCase.DoesNotExist:
        return generic_500(request=request)

    return redirect('ai_use_case')
