from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect

from core.models.meeting_note import MeetingNote


def meeting_delete_note_view(request: HttpRequest, note_id: int) -> HttpResponse:
    """Delete a meeting note."""
    note = get_object_or_404(MeetingNote, pk=note_id)
    meeting_id = note.meeting.id
    note.delete()
    return redirect(to='meeting_detail', model_id=meeting_id)
