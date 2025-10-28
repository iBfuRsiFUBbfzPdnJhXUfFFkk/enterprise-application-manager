from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.models.estimation import Estimation
from core.views.generic.generic_500 import generic_500


def estimation_delete_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        estimation = Estimation.objects.get(id=model_id)
        estimation.delete()
    except Estimation.DoesNotExist:
        return generic_500(request=request)

    return redirect(to='estimation')
