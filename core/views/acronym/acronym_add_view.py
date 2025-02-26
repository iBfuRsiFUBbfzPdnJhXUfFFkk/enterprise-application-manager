from django.http import HttpRequest, HttpResponse

from core.forms.acronym_form import AcronymForm
from core.views.generic.generic_add_view import generic_add_view


def acronym_add_view(request: HttpRequest) -> HttpResponse:
    return generic_add_view(
        form_cls=AcronymForm,
        request=request,
        success_route='acronym',
    )
