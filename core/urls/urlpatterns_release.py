from django.urls import URLPattern, URLResolver, path

from core.views.release.release_add_view import release_add_view
from core.views.release.release_detail_view import release_detail_view
from core.views.release.release_edit_view import release_edit_view
from core.views.release.release_view import release_view

urlpatterns_release: list[URLPattern | URLResolver] = [
    path("release/", release_view, name="release"),
    path("release/edit/<int:model_id>/", release_edit_view, name="release_edit"),
    path("release/new/", release_add_view, name="release_new"),
    path("release/detail/<int:model_id>/", release_detail_view, name="release_detail"),
]
