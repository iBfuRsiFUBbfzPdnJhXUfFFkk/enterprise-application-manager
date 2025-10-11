from django.http import HttpRequest, HttpResponse

from core.models.requirement import Requirement
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def requirement_detail_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        requirement = Requirement.objects.get(id=model_id)
        historical_records = requirement.history.all()
    except Requirement.DoesNotExist:
        return generic_500(request=request)

    return base_render(
        request=request,
        template_name='authenticated/requirement/requirement_detail.html',
        context={
            'requirement': requirement,
            'historical_records': historical_records,
        }
    )
