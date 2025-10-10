from typing import Mapping, Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.billing_code_form import BillingCodeForm
from core.models.billing_code import BillingCode
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def billing_code_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        billing_code = BillingCode.objects.get(id=model_id)
    except BillingCode.DoesNotExist:
        return generic_500(request=request)

    if request.method == 'POST':
        form = BillingCodeForm(request.POST, instance=billing_code)
        if form.is_valid():
            form.save()
            return redirect(to='billing_code')
    else:
        form = BillingCodeForm(instance=billing_code)

    context: Mapping[str, Any] = {'form': form}
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/billing_code/billing_code_form.html'
    )
