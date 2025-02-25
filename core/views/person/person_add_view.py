from django.http import HttpRequest, HttpResponse

from core.forms.person_form import PersonForm
from core.views.generic.generic_add_view import generic_add_view


def person_add_view(request: HttpRequest) -> HttpResponse:
    return generic_add_view(
        form_cls=PersonForm,
        request=request,
        success_route='person',
    )
