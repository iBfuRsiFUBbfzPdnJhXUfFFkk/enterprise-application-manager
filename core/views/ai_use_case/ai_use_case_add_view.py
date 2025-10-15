from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.ai_use_case_form import AIUseCaseForm
from core.utilities.base_render import base_render


def ai_use_case_add_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = AIUseCaseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ai_use_case')
    else:
        form = AIUseCaseForm()

    return base_render(
        request=request,
        template_name='authenticated/ai_use_case/ai_use_case_form.html',
        context={'form': form}
    )
