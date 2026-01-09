from typing import Any, Mapping

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404

from core.forms.meeting_action_item_form import MeetingActionItemInlineForm
from core.forms.meeting_note_form import MeetingNoteForm
from core.models.meeting import Meeting
from core.utilities.base_render import base_render


def meeting_detail_view(request: HttpRequest, model_id: int) -> HttpResponse:
    """Detail view for a meeting with action items and notes."""
    meeting = get_object_or_404(
        Meeting.objects.select_related('organizer', 'application', 'project').prefetch_related(
            'attendees', 'actual_attendees', 'action_items__assignee', 'notes__person'
        ),
        pk=model_id,
    )

    action_item_form = MeetingActionItemInlineForm()
    note_form = MeetingNoteForm()

    context: Mapping[str, Any] = {
        'meeting': meeting,
        'action_item_form': action_item_form,
        'note_form': note_form,
    }
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/meeting/meeting_detail.html',
    )
