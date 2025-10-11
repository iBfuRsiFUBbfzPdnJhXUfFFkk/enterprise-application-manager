from django.http import HttpRequest, HttpResponse

from core.models.onboard_procedure import OnboardProcedure
from core.views.generic.generic_view import generic_view


def onboard_procedure_view(request: HttpRequest) -> HttpResponse:
    return generic_view(
        additional_context={'onboard_procedures': OnboardProcedure.objects.all()},
        model_cls=OnboardProcedure,
        name='onboard_procedure',
        request=request,
    )
