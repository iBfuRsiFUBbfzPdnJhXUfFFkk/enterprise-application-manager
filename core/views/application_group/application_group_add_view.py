from django.http import HttpRequest, HttpResponse

from core.forms.application_group_form import ApplicationGroupForm
from core.views.generic.generic_add_view import generic_add_view


def application_group_add_view(request: HttpRequest) -> HttpResponse:
    return generic_add_view(
        form_cls=ApplicationGroupForm,
        request=request,
        success_route='application_group',
    )
