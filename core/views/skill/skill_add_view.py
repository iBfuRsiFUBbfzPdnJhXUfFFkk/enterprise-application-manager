from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.skill_form import SkillForm
from core.utilities.base_render import base_render


def skill_add_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('skill')
    else:
        form = SkillForm()

    return base_render(
        request=request,
        template_name='authenticated/skill/skill_form.html',
        context={'form': form}
    )
