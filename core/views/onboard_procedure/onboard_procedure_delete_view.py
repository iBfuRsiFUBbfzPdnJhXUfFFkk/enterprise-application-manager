from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.models.onboard_procedure import OnboardProcedure
from core.views.generic.generic_500 import generic_500


def onboard_procedure_delete_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        onboard_procedure = OnboardProcedure.objects.get(id=model_id)
        onboard_procedure.delete()
    except OnboardProcedure.DoesNotExist:
        return generic_500(request=request)

    return redirect('onboard_procedure')
