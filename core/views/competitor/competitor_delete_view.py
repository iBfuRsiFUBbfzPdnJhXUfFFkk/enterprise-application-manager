from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.models.competitor import Competitor
from core.views.generic.generic_500 import generic_500


def competitor_delete_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        competitor = Competitor.objects.get(id=model_id)
        competitor.delete()
    except Competitor.DoesNotExist:
        return generic_500(request=request)

    return redirect('competitor')
