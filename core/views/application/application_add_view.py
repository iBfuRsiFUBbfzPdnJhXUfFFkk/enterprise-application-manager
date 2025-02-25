from django.http import HttpRequest, HttpResponse

from core.forms.application_form import ApplicationForm
from core.views.generic.generic_add_view import generic_add_view


def application_add_view(request: HttpRequest) -> HttpResponse:
    return generic_add_view(
        form_cls=ApplicationForm,
        request=request,
        success_route='application',
    )
