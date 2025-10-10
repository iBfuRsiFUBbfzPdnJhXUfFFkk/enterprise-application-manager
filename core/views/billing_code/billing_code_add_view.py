from typing import Mapping, Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.billing_code_form import BillingCodeForm
from core.utilities.base_render import base_render


def billing_code_add_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = BillingCodeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='billing_code')
    else:
        form = BillingCodeForm()

    context: Mapping[str, Any] = {'form': form}
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/billing_code/billing_code_form.html'
    )
