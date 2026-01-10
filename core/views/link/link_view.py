from django.db.models import Exists, OuterRef
from django.http import HttpRequest, HttpResponse

from core.models.link import Link
from core.models.user_bookmark import UserBookmark
from core.views.generic.generic_view import generic_view


def link_view(request: HttpRequest) -> HttpResponse:
    # Annotate each link with whether the current user has bookmarked it
    user_bookmarks = UserBookmark.objects.filter(
        link=OuterRef('pk'),
        user=request.user
    )

    links = Link.objects.all().annotate(
        is_bookmarked_by_current_user=Exists(user_bookmarks)
    ).prefetch_related('user_bookmarks__user')

    return generic_view(
        additional_context={
            'links': links,
            'user': request.user,
        },
        model_cls=Link,
        name='link',
        request=request,
    )
