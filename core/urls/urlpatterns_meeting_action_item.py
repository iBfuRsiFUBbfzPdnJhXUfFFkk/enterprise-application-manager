from django.urls import URLPattern, URLResolver, path

from core.views.meeting_action_item import (
    meeting_action_item_add_view,
    meeting_action_item_delete_view,
    meeting_action_item_detail_view,
    meeting_action_item_edit_view,
    meeting_action_item_view,
)

urlpatterns_meeting_action_item: list[URLPattern | URLResolver] = [
    path("meeting_action_item/", meeting_action_item_view, name="meeting_action_item"),
    path("meeting_action_item/edit/<int:model_id>/", meeting_action_item_edit_view, name="meeting_action_item_edit"),
    path("meeting_action_item/new/", meeting_action_item_add_view, name="meeting_action_item_new"),
    path("meeting-action-item/<int:model_id>/", meeting_action_item_detail_view, name="meeting_action_item_detail"),
    path("meeting-action-item/delete/<int:model_id>/", meeting_action_item_delete_view, name="meeting_action_item_delete"),
]
