from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.models.risk import Risk
from core.views.generic.generic_500 import generic_500


def risk_delete_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        risk = Risk.objects.get(id=model_id)
        risk.delete()
    except Risk.DoesNotExist:
        return generic_500(request=request)

    return redirect('risk')
