from django.urls import URLPattern, URLResolver, path

from core.urls.common.create_generic_urlpatterns import create_generic_urlpatterns
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

urlpatterns_meeting: list[URLPattern | URLResolver] = create_generic_urlpatterns(
    name='meeting',
    view=meeting_view,
    view_edit=meeting_edit_view,
    view_new=meeting_add_view,
)

urlpatterns_meeting.extend(
    [
        path(name='meeting_detail', route='meeting/<int:model_id>/', view=meeting_detail_view),
        path(name='meeting_delete', route='meeting/delete/<int:model_id>/', view=meeting_delete_view),
        path(
            name='meeting_add_action_item',
            route='meeting/<int:model_id>/add-action-item/',
            view=meeting_add_action_item_view,
        ),
        path(
            name='meeting_add_note',
            route='meeting/<int:model_id>/add-note/',
            view=meeting_add_note_view,
        ),
        path(
            name='meeting_delete_note',
            route='meeting/note/delete/<int:note_id>/',
            view=meeting_delete_note_view,
        ),
        path(
            name='meeting_update_minutes',
            route='meeting/<int:model_id>/update-minutes/',
            view=meeting_update_minutes_view,
        ),
        path(
            name='meeting_toggle_attendance',
            route='meeting/<int:model_id>/toggle-attendance/<int:person_id>/',
            view=meeting_toggle_attendance_view,
        ),
    ]
)
