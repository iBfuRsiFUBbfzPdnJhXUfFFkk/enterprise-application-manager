from django.http import HttpRequest, HttpResponse

from core.forms.release_form import ReleaseForm
from core.models.release import Release
from core.views.generic.generic_edit_view import generic_edit_view


def release_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    return generic_edit_view(
        form_cls=ReleaseForm,
        model_cls=Release,
        model_id=model_id,
        request=request,
        success_route='release',
    )
