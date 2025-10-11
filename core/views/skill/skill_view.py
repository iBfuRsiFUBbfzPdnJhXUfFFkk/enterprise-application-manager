from django.http import HttpRequest, HttpResponse

from core.models.skill import Skill
from core.views.generic.generic_view import generic_view


def skill_view(request: HttpRequest) -> HttpResponse:
    return generic_view(
        model_cls=Skill,
        name='skill',
        request=request,
    )
