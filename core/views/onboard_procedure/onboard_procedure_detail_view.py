from django.http import HttpRequest, HttpResponse

from core.models.onboard_procedure import OnboardProcedure
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def onboard_procedure_detail_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        onboard_procedure = OnboardProcedure.objects.get(id=model_id)
        historical_records = onboard_procedure.history.all()
    except OnboardProcedure.DoesNotExist:
        return generic_500(request=request)

    return base_render(
        request=request,
        template_name='authenticated/onboard_procedure/onboard_procedure_detail.html',
        context={
            'onboard_procedure': onboard_procedure,
            'historical_records': historical_records,
        }
    )
