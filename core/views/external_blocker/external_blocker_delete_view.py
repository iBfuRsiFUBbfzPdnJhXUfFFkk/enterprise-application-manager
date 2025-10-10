from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.models.external_blockers import ExternalBlockers
from core.views.generic.generic_500 import generic_500


def external_blocker_delete_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        external_blocker = ExternalBlockers.objects.get(id=model_id)
        external_blocker.delete()
    except ExternalBlockers.DoesNotExist:
        return generic_500(request=request)

    return redirect(to='external_blocker')
