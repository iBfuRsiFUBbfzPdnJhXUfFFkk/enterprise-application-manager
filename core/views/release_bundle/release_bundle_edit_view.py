from django.http import HttpRequest, HttpResponse

from core.forms.release_bundle_form import ReleaseBundleForm
from core.models.release_bundle import ReleaseBundle
from core.views.generic.generic_edit_view import generic_edit_view


def release_bundle_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    return generic_edit_view(
        form_cls=ReleaseBundleForm,
        model_cls=ReleaseBundle,
        model_id=model_id,
        request=request,
        success_route='release_bundle',
    )
