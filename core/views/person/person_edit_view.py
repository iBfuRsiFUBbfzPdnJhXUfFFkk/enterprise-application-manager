from django.http import HttpRequest, HttpResponse

from core.forms import PersonForm
from core.models.person import Person
from core.views.generic.generic_edit_view import generic_edit_view


def person_edit_view(request: HttpRequest, person_id: int) -> HttpResponse:
    return generic_edit_view(
        form_cls=PersonForm,
        model_cls=Person,
        model_id=person_id,
        request=request,
        success_route='person',
    )