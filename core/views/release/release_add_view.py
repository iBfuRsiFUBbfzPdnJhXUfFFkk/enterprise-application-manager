from django.http import HttpRequest, HttpResponse

from core.forms.release_form import ReleaseForm
from core.views.generic.generic_add_view import generic_add_view


def release_add_view(request: HttpRequest) -> HttpResponse:
    return generic_add_view(
        form_cls=ReleaseForm,
        request=request,
        success_route='release',
    )
