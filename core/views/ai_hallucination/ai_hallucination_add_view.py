from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.ai_hallucination_form import AIHallucinationForm
from core.utilities.base_render import base_render


def ai_hallucination_add_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = AIHallucinationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ai_hallucination')
    else:
        form = AIHallucinationForm()

    return base_render(
        request=request,
        template_name='authenticated/ai_hallucination/ai_hallucination_form.html',
        context={'form': form}
    )
