from typing import Mapping, Any
from django.http import HttpRequest, HttpResponse

from core.models.formula import Formula
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def formula_detail_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        formula = Formula.objects.get(id=model_id)
    except Formula.DoesNotExist:
        return generic_500(request=request)

    # Get historical records
    historical_records = formula.history.all()

    context: Mapping[str, Any] = {
        'formula': formula,
        'historical_records': historical_records,
    }
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/formula/formula_detail.html'
    )
