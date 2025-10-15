from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.models.ai_vendor import AIVendor
from core.views.generic.generic_500 import generic_500


def ai_vendor_delete_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        ai_vendor = AIVendor.objects.get(id=model_id)
        ai_vendor.delete()
    except AIVendor.DoesNotExist:
        return generic_500(request=request)

    return redirect('ai_vendor')
