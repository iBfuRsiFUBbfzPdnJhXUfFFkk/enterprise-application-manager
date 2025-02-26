from django.http import HttpRequest, HttpResponse

from core.forms.dependency_form import DependencyForm
from core.views.generic.generic_add_view import generic_add_view


def dependency_add_view(request: HttpRequest) -> HttpResponse:
    return generic_add_view(
        form_cls=DependencyForm,
        request=request,
        success_route='dependency',
    )
