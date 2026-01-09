from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect

from core.forms.meeting_note_form import MeetingNoteForm
from core.models.meeting import Meeting


def meeting_add_note_view(request: HttpRequest, model_id: int) -> HttpResponse:
    """Add a note or quote to a meeting from the detail page."""
    meeting = get_object_or_404(Meeting, pk=model_id)

    if request.method == 'POST':
        form = MeetingNoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.meeting = meeting
            note.save()

    return redirect(to='meeting_detail', model_id=model_id)
