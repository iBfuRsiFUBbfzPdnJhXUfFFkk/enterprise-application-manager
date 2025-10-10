from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.models.billing_code import BillingCode
from core.views.generic.generic_500 import generic_500


def billing_code_delete_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        billing_code = BillingCode.objects.get(id=model_id)
        billing_code.delete()
    except BillingCode.DoesNotExist:
        return generic_500(request=request)

    return redirect(to='billing_code')
