from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.models.skill import Skill
from core.views.generic.generic_500 import generic_500


def skill_delete_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        skill = Skill.objects.get(id=model_id)
        skill.delete()
    except Skill.DoesNotExist:
        return generic_500(request=request)

    return redirect('skill')
