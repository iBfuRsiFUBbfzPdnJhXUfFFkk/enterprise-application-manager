from django.http import HttpRequest, HttpResponse

from core.models.release import Release
from core.views.generic.generic_detail_view import generic_detail_view


def release_detail_view(request: HttpRequest, model_id: int) -> HttpResponse:
    return generic_detail_view(
        model_cls=Release,
        model_id=model_id,
        request=request,
        template_name='authenticated/release/release_detail.html',
    )
