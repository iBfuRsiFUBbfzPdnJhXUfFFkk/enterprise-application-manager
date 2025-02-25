from django.http import HttpRequest, HttpResponse

from core.forms.application_form import ApplicationForm
from core.models.application import Application
from core.views.generic.generic_edit_view import generic_edit_view


def application_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    return generic_edit_view(
        form_cls=ApplicationForm,
        model_cls=Application,
        model_id=model_id,
        request=request,
        success_route='application',
    )
