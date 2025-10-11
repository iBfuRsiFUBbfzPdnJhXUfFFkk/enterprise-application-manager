from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.models.requirement import Requirement
from core.views.generic.generic_500 import generic_500


def requirement_delete_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        requirement = Requirement.objects.get(id=model_id)
        requirement.delete()
    except Requirement.DoesNotExist:
        return generic_500(request=request)

    return redirect('requirement')
