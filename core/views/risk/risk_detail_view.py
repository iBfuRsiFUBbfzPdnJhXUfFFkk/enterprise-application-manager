from django.http import HttpRequest, HttpResponse

from core.models.risk import Risk
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def risk_detail_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        risk = Risk.objects.get(id=model_id)
        historical_records = risk.history.all()
    except Risk.DoesNotExist:
        return generic_500(request=request)

    return base_render(
        request=request,
        template_name='authenticated/risk/risk_detail.html',
        context={
            'risk': risk,
            'historical_records': historical_records,
        }
    )
