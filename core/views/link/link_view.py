from django.http import HttpRequest, HttpResponse

from core.models.link import Link
from core.views.generic.generic_view import generic_view


def link_view(request: HttpRequest) -> HttpResponse:
    # Prefetch bookmarked_by to avoid N+1 queries
    links = Link.objects.all().prefetch_related('bookmarked_by')

    return generic_view(
        additional_context={
            'links': links,
            'user': request.user,
        },
        model_cls=Link,
        name='link',
        request=request,
    )
