from django.http import HttpRequest, HttpResponse

from core.models.acronym import Acronym
from core.views.generic.generic_delete_view import generic_delete_view


def acronym_delete_view(request: HttpRequest, model_id: int) -> HttpResponse:
    return generic_delete_view(
        model_cls=Acronym,
        model_id=model_id,
        request=request,
        success_route='acronym',
    )
