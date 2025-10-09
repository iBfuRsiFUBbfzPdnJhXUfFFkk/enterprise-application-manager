from django.urls import URLPattern, URLResolver, path

from core.urls.common.create_generic_urlpatterns import create_generic_urlpatterns
from core.views.release_bundle.release_bundle_add_view import release_bundle_add_view
from core.views.release_bundle.release_bundle_detail_view import release_bundle_detail_view
from core.views.release_bundle.release_bundle_edit_view import release_bundle_edit_view
from core.views.release_bundle.release_bundle_view import release_bundle_view

urlpatterns_release_bundle: list[URLPattern | URLResolver] = [
    *create_generic_urlpatterns(
        name="release_bundle",
        view=release_bundle_view,
        view_edit=release_bundle_edit_view,
        view_new=release_bundle_add_view,
    ),
    path(name="release_bundle_detail", route="release_bundle/<int:model_id>/", view=release_bundle_detail_view),
    path(name="release_bundle_edit", route="release_bundle/edit/<int:model_id>/", view=release_bundle_edit_view),
]
