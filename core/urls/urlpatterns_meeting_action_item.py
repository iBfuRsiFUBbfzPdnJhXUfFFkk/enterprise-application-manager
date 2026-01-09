from django.urls import URLPattern, URLResolver, path

from core.urls.common.create_generic_urlpatterns import create_generic_urlpatterns
from core.views.meeting_action_item import (
    meeting_action_item_add_view,
    meeting_action_item_delete_view,
    meeting_action_item_detail_view,
    meeting_action_item_edit_view,
    meeting_action_item_view,
)

urlpatterns_meeting_action_item: list[URLPattern | URLResolver] = create_generic_urlpatterns(
    name='meeting_action_item',
    view=meeting_action_item_view,
    view_edit=meeting_action_item_edit_view,
    view_new=meeting_action_item_add_view,
)

urlpatterns_meeting_action_item.extend(
    [
        path(
            name='meeting_action_item_detail',
            route='meeting-action-item/<int:model_id>/',
            view=meeting_action_item_detail_view,
        ),
        path(
            name='meeting_action_item_delete',
            route='meeting-action-item/delete/<int:model_id>/',
            view=meeting_action_item_delete_view,
        ),
    ]
)
