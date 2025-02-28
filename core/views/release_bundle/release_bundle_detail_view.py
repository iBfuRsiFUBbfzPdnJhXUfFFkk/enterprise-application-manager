from django.http import HttpRequest, HttpResponse

from core.models.release_bundle import ReleaseBundle
from core.views.generic.generic_detail_view import generic_detail_view


def release_bundle_detail_view(request: HttpRequest, model_id: int) -> HttpResponse:
    return generic_detail_view(
        model_cls=ReleaseBundle,
        model_id=model_id,
        request=request,
        template_name='release_bundle/release_bundle_detail.html',
    )
