from django.http import HttpRequest, HttpResponse

from core.models.ai_vendor import AIVendor
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def ai_vendor_detail_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        ai_vendor = AIVendor.objects.get(id=model_id)
        historical_records = ai_vendor.history.all()
    except AIVendor.DoesNotExist:
        return generic_500(request=request)

    return base_render(
        request=request,
        template_name='authenticated/ai_vendor/ai_vendor_detail.html',
        context={
            'ai_vendor': ai_vendor,
            'historical_records': historical_records,
        }
    )
