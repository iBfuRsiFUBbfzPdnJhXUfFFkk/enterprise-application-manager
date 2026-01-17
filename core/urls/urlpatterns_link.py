from django.urls import URLPattern, URLResolver, path

from core.views.bookmark_folder import (
    bookmark_folder_create_ajax_view,
    bookmark_folder_delete_ajax_view,
    bookmark_folder_rename_ajax_view,
    bookmark_folder_reorder_ajax_view,
    bookmark_move_ajax_view,
    bookmark_view_preference_toggle_view,
)
from core.views.link import (
    link_add_view,
    link_bookmark_modal_view,
    link_bookmark_toggle_view,
    link_create_ajax_view,
    link_delete_ajax_view,
    link_delete_view,
    link_detail_view,
    link_edit_ajax_view,
    link_edit_view,
    link_view,
)

urlpatterns_link: list[URLPattern | URLResolver] = [
    path("link/", link_view, name="link"),
    path("link/edit/<int:model_id>/", link_edit_view, name="link_edit"),
    path("link/new/", link_add_view, name="link_new"),
    path("link/<int:model_id>/", link_detail_view, name="link_detail"),
    path("link/delete/<int:model_id>/", link_delete_view, name="link_delete"),
    path("link/create/ajax/", link_create_ajax_view, name="link_create_ajax"),
    path("link/<int:link_id>/edit/ajax/", link_edit_ajax_view, name="link_edit_ajax"),
    path("link/<int:link_id>/delete/ajax/", link_delete_ajax_view, name="link_delete_ajax"),
    path("link/<int:link_id>/bookmark/toggle/", link_bookmark_toggle_view, name="link_bookmark_toggle"),
    path("link/bookmark/modal/", link_bookmark_modal_view, name="link_bookmark_modal"),
    path("bookmark/folder/create/", bookmark_folder_create_ajax_view, name="bookmark_folder_create"),
    path("bookmark/folder/<int:folder_id>/delete/", bookmark_folder_delete_ajax_view, name="bookmark_folder_delete"),
    path("bookmark/folder/<int:folder_id>/rename/", bookmark_folder_rename_ajax_view, name="bookmark_folder_rename"),
    path("bookmark/folder/reorder/", bookmark_folder_reorder_ajax_view, name="bookmark_folder_reorder"),
    path("bookmark/move/", bookmark_move_ajax_view, name="bookmark_move"),
    path("bookmark/view-preference/toggle/", bookmark_view_preference_toggle_view, name="bookmark_view_preference_toggle"),
]
