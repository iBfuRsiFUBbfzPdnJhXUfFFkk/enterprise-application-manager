from django.http import HttpRequest, HttpResponse

from core.forms.application_group_form import ApplicationGroupForm
from core.models.application_group import ApplicationGroup
from core.views.generic.generic_edit_view import generic_edit_view


def application_group_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    return generic_edit_view(
        form_cls=ApplicationGroupForm,
        model_cls=ApplicationGroup,
        model_id=model_id,
        request=request,
        success_route='application_group',
    )
