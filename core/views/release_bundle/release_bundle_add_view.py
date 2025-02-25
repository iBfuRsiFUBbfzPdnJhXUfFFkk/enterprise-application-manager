from django.http import HttpRequest, HttpResponse

from core.forms.release_bundle_form import ReleaseBundleForm
from core.views.generic.generic_add_view import generic_add_view


def release_bundle_add_view(request: HttpRequest) -> HttpResponse:
    return generic_add_view(
        form_cls=ReleaseBundleForm,
        request=request,
        success_route='release_bundle',
    )
