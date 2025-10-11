from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.models.sprint import Sprint
from core.views.generic.generic_500 import generic_500


def sprint_delete_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        sprint = Sprint.objects.get(id=model_id)
        sprint.delete()
    except Sprint.DoesNotExist:
        return generic_500(request=request)

    return redirect('sprint')
