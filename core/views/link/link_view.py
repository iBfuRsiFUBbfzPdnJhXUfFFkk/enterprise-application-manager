from django.http import HttpRequest, HttpResponse

from core.models.link import Link
from core.views.generic.generic_view import generic_view


def link_view(request: HttpRequest) -> HttpResponse:
    return generic_view(
        additional_context={'links': Link.objects.all()},
        model_cls=Link,
        name='link',
        request=request,
    )
