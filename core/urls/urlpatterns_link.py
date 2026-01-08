from django.urls import URLPattern, URLResolver, path

from core.urls.common.create_generic_urlpatterns import create_generic_urlpatterns
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
    link_delete_view,
    link_detail_view,
    link_edit_view,
    link_view,
)

urlpatterns_link: list[URLPattern | URLResolver] = create_generic_urlpatterns(
    name='link',
    view=link_view,
    view_edit=link_edit_view,
    view_new=link_add_view,
)

# Add detail view
urlpatterns_link.append(
    path(name='link_detail', route='link/<int:model_id>/', view=link_detail_view)
)

# Add delete view
urlpatterns_link.append(
    path(name='link_delete', route='link/delete/<int:model_id>/', view=link_delete_view)
)

# Add AJAX create view
urlpatterns_link.append(
    path(name='link_create_ajax', route='link/create/ajax/', view=link_create_ajax_view)
)

# Add bookmark toggle endpoint
urlpatterns_link.append(
    path(name='link_bookmark_toggle', route='link/<int:link_id>/bookmark/toggle/', view=link_bookmark_toggle_view)
)

# Add bookmark modal data endpoint
urlpatterns_link.append(
    path(name='link_bookmark_modal', route='link/bookmark/modal/', view=link_bookmark_modal_view)
)

# Bookmark folder endpoints
urlpatterns_link.append(
    path(name='bookmark_folder_create', route='bookmark/folder/create/', view=bookmark_folder_create_ajax_view)
)
urlpatterns_link.append(
    path(name='bookmark_folder_delete', route='bookmark/folder/<int:folder_id>/delete/', view=bookmark_folder_delete_ajax_view)
)
urlpatterns_link.append(
    path(name='bookmark_folder_rename', route='bookmark/folder/<int:folder_id>/rename/', view=bookmark_folder_rename_ajax_view)
)
urlpatterns_link.append(
    path(name='bookmark_folder_reorder', route='bookmark/folder/reorder/', view=bookmark_folder_reorder_ajax_view)
)
urlpatterns_link.append(
    path(name='bookmark_move', route='bookmark/move/', view=bookmark_move_ajax_view)
)
urlpatterns_link.append(
    path(name='bookmark_view_preference_toggle', route='bookmark/view-preference/toggle/', view=bookmark_view_preference_toggle_view)
)
