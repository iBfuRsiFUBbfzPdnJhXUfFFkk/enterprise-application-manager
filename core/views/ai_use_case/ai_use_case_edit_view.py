from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.ai_use_case_form import AIUseCaseForm
from core.models.ai_use_case import AIUseCase
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def ai_use_case_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        ai_use_case = AIUseCase.objects.get(id=model_id)
    except AIUseCase.DoesNotExist:
        return generic_500(request=request)

    if request.method == 'POST':
        form = AIUseCaseForm(request.POST, instance=ai_use_case)
        if form.is_valid():
            form.save()
            return redirect('ai_use_case')
    else:
        form = AIUseCaseForm(instance=ai_use_case)

    return base_render(
        request=request,
        template_name='authenticated/ai_use_case/ai_use_case_form.html',
        context={'form': form}
    )
