from django.urls import URLPattern, URLResolver, path

from core.urls.common.create_generic_urlpatterns import create_generic_urlpatterns
from core.views.release.release_add_view import release_add_view
from core.views.release.release_detail_view import release_detail_view
from core.views.release.release_edit_view import release_edit_view
from core.views.release.release_view import release_view

urlpatterns_release: list[URLPattern | URLResolver] = [
    *create_generic_urlpatterns(
        name="release",
        view=release_view,
        view_edit=release_edit_view,
        view_new=release_add_view,
    ),
    path(name="release_detail", route="release/detail/<int:model_id>/", view=release_detail_view),
]
