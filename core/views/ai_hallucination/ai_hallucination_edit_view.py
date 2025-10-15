from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.ai_hallucination_form import AIHallucinationForm
from core.models.ai_hallucination import AIHallucination
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def ai_hallucination_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        ai_hallucination = AIHallucination.objects.get(id=model_id)
    except AIHallucination.DoesNotExist:
        return generic_500(request=request)

    if request.method == 'POST':
        form = AIHallucinationForm(request.POST, instance=ai_hallucination)
        if form.is_valid():
            form.save()
            return redirect('ai_hallucination')
    else:
        form = AIHallucinationForm(instance=ai_hallucination)

    return base_render(
        request=request,
        template_name='authenticated/ai_hallucination/ai_hallucination_form.html',
        context={'form': form}
    )
