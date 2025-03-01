from django.http import HttpRequest, HttpResponse

from core.models.release_bundle import ReleaseBundle
from core.views.generic.generic_view import generic_view


def release_bundle_view(request: HttpRequest) -> HttpResponse:
    return generic_view(
        context_name="release_bundles",
        model_cls=ReleaseBundle,
        request=request,
        template_name='authenticated/release_bundle/release_bundle.html',
    )
