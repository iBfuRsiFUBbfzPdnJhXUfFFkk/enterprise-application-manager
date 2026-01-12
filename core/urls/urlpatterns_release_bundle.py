from django.urls import URLPattern, URLResolver, path

from core.views.release_bundle.release_bundle_add_view import release_bundle_add_view
from core.views.release_bundle.release_bundle_detail_view import release_bundle_detail_view
from core.views.release_bundle.release_bundle_edit_view import release_bundle_edit_view
from core.views.release_bundle.release_bundle_view import release_bundle_view

urlpatterns_release_bundle: list[URLPattern | URLResolver] = [
    path("release_bundle/", release_bundle_view, name="release_bundle"),
    path("release_bundle/edit/<int:model_id>/", release_bundle_edit_view, name="release_bundle_edit"),
    path("release_bundle/new/", release_bundle_add_view, name="release_bundle_new"),
    path("release_bundle/<int:model_id>/", release_bundle_detail_view, name="release_bundle_detail"),
]
