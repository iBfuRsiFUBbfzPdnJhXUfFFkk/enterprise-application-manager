from django.urls import URLPattern, URLResolver, path

from core.views.meeting import (
    meeting_add_action_item_view,
    meeting_add_note_view,
    meeting_add_view,
    meeting_delete_note_view,
    meeting_delete_view,
    meeting_detail_view,
    meeting_edit_view,
    meeting_toggle_attendance_view,
    meeting_update_minutes_view,
    meeting_view,
)

urlpatterns_meeting: list[URLPattern | URLResolver] = [
    path("meeting/", meeting_view, name="meeting"),
    path("meeting/edit/<int:model_id>/", meeting_edit_view, name="meeting_edit"),
    path("meeting/new/", meeting_add_view, name="meeting_new"),
    path("meeting/<int:model_id>/", meeting_detail_view, name="meeting_detail"),
    path("meeting/delete/<int:model_id>/", meeting_delete_view, name="meeting_delete"),
    path("meeting/<int:model_id>/add-action-item/", meeting_add_action_item_view, name="meeting_add_action_item"),
    path("meeting/<int:model_id>/add-note/", meeting_add_note_view, name="meeting_add_note"),
    path("meeting/note/delete/<int:note_id>/", meeting_delete_note_view, name="meeting_delete_note"),
    path("meeting/<int:model_id>/update-minutes/", meeting_update_minutes_view, name="meeting_update_minutes"),
    path("meeting/<int:model_id>/toggle-attendance/<int:person_id>/", meeting_toggle_attendance_view, name="meeting_toggle_attendance"),
]
