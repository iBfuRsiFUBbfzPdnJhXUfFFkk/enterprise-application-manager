from django.http import HttpRequest, HttpResponse

from core.models.competitor import Competitor
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def competitor_detail_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        competitor = Competitor.objects.get(id=model_id)
        historical_records = competitor.history.all()
    except Competitor.DoesNotExist:
        return generic_500(request=request)

    return base_render(
        request=request,
        template_name='authenticated/competitor/competitor_detail.html',
        context={
            'competitor': competitor,
            'historical_records': historical_records,
        }
    )
