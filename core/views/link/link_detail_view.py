from django.http import HttpRequest, HttpResponse

from core.models.link import Link
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def link_detail_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        link = Link.objects.prefetch_related('bookmarked_by').get(id=model_id)
        historical_records = link.history.all()
        is_bookmarked = link.bookmarked_by.filter(id=request.user.id).exists()
    except Link.DoesNotExist:
        return generic_500(request=request)

    return base_render(
        request=request,
        template_name='authenticated/link/link_detail.html',
        context={
            'link': link,
            'historical_records': historical_records,
            'is_bookmarked': is_bookmarked,
        }
    )
