from django.http import HttpRequest, HttpResponse

from core.forms.person_form import PersonForm
from core.models.person import Person
from core.views.generic.generic_edit_view import generic_edit_view


def person_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    return generic_edit_view(
        form_cls=PersonForm,
        model_cls=Person,
        model_id=model_id,
        request=request,
        success_route='person',
    )
