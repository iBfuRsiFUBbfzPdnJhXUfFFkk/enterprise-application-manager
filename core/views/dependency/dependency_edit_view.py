from django.http import HttpRequest, HttpResponse

from core.forms.dependency_form import DependencyForm
from core.models.dependency import Dependency
from core.views.generic.generic_edit_view import generic_edit_view


def dependency_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    return generic_edit_view(
        form_cls=DependencyForm,
        model_cls=Dependency,
        model_id=model_id,
        request=request,
        success_route='dependency',
    )
