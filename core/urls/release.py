from django.urls import URLPattern, URLResolver, path

from core.views.release.release_add_view import release_add_view
from core.views.release.release_detail_view import release_detail_view
from core.views.release.release_edit_view import release_edit_view
from core.views.release.release_view import release_view

urlpatterns_release: list[URLPattern | URLResolver] = [
    path(name="release", route="release", view=release_view),
    path(name="release_detail", route="release/detail/<int:model_id>", view=release_detail_view),
    path(name="release_edit", route="release/edit/<int:model_id>", view=release_edit_view),
    path(name="release_new", route="release/new", view=release_add_view),
]
