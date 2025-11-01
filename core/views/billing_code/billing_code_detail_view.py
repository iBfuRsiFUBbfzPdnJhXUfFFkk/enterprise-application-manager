from typing import Mapping, Any
from django.http import HttpRequest, HttpResponse

from core.models.billing_code import BillingCode
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def billing_code_detail_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        billing_code = BillingCode.objects.get(id=model_id)
    except BillingCode.DoesNotExist:
        return generic_500(request=request)

    # Get historical records
    historical_records = billing_code.history.all()

    # Get billing codes that replace this one
    replaced_by_codes = billing_code.replaced_by_codes.all()

    context: Mapping[str, Any] = {
        'billing_code': billing_code,
        'historical_records': historical_records,
        'replaced_by_codes': replaced_by_codes,
    }
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/billing_code/billing_code_detail.html'
    )
