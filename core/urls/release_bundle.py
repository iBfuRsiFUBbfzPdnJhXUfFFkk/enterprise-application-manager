from django.urls import URLPattern, URLResolver, path

from core.views.release_bundle.release_bundle_add_view import release_bundle_add_view
from core.views.release_bundle.release_bundle_detail_view import release_bundle_detail_view
from core.views.release_bundle.release_bundle_edit_view import release_bundle_edit_view
from core.views.release_bundle.release_bundle_view import release_bundle_view

urlpatterns_release_bundle: list[URLPattern | URLResolver] = [
    path(name="release_bundle", route="release_bundle", view=release_bundle_view),
    path(name="release_bundle_detail", route="release_bundle/detail/<int:model_id>", view=release_bundle_detail_view),
    path(name="release_bundle_edit", route="release_bundle/edit/<int:model_id>", view=release_bundle_edit_view),
    path(name="release_bundle_new", route="release_bundle/new", view=release_bundle_add_view),
]
