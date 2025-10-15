from django.http import HttpRequest, HttpResponse

from core.models.ai_vendor import AIVendor
from core.views.generic.generic_view import generic_view


def ai_vendor_view(request: HttpRequest) -> HttpResponse:
    return generic_view(
        model_cls=AIVendor,
        name='ai_vendor',
        request=request,
    )
