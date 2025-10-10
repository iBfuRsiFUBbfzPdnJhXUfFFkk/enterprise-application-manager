from django.http import HttpRequest, HttpResponse

from core.models.billing_code import BillingCode
from core.views.generic.generic_view import generic_view


def billing_code_view(request: HttpRequest) -> HttpResponse:
    return generic_view(
        model_cls=BillingCode,
        name='billing_code',
        request=request,
    )
