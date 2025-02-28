from django.http import HttpRequest, HttpResponse

from core.forms.acronym_form import AcronymForm
from core.models.acronym import Acronym
from core.views.generic.generic_edit_view import generic_edit_view


def acronym_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    return generic_edit_view(
        form_cls=AcronymForm,
        model_cls=Acronym,
        model_id=model_id,
        request=request,
        success_route='acronym',
    )
