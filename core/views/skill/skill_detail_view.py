from django.http import HttpRequest, HttpResponse

from core.models.skill import Skill
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def skill_detail_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        skill = Skill.objects.get(id=model_id)
        historical_records = skill.history.all()
    except Skill.DoesNotExist:
        return generic_500(request=request)

    return base_render(
        request=request,
        template_name='authenticated/skill/skill_detail.html',
        context={
            'skill': skill,
            'historical_records': historical_records,
        }
    )
