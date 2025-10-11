from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.skill_form import SkillForm
from core.models.skill import Skill
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def skill_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        skill = Skill.objects.get(id=model_id)
    except Skill.DoesNotExist:
        return generic_500(request=request)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            return redirect('skill')
    else:
        form = SkillForm(instance=skill)

    return base_render(
        request=request,
        template_name='authenticated/skill/skill_form.html',
        context={'form': form}
    )
