from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse

from core.models.billing_code import BillingCode
from core.utilities.base_render import base_render


def billing_code_view(request: HttpRequest) -> HttpResponse:
    # Get filter parameter - defaults to showing only active billing codes
    show_inactive = request.GET.get('show_inactive', 'false').lower() == 'true'

    # Filter billing codes based on the parameter
    if show_inactive:
        models: QuerySet = BillingCode.objects.all()
    else:
        models: QuerySet = BillingCode.objects.filter(is_active=True)

    context = {
        'models': models,
        'show_inactive': show_inactive,
    }

    return base_render(
        context=context,
        request=request,
        template_name='authenticated/billing_code/billing_code.html'
    )
