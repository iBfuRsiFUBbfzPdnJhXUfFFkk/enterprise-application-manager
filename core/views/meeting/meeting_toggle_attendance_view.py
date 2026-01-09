from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect

from core.models.meeting import Meeting
from core.models.person import Person


def meeting_toggle_attendance_view(request: HttpRequest, model_id: int, person_id: int) -> HttpResponse:
    """Toggle a person's attendance status for roll call."""
    meeting = get_object_or_404(Meeting, pk=model_id)
    person = get_object_or_404(Person, pk=person_id)

    if request.method == 'POST':
        if meeting.actual_attendees.filter(pk=person_id).exists():
            # Person is marked as attended, remove them
            meeting.actual_attendees.remove(person)
        else:
            # Person is not marked as attended, add them
            meeting.actual_attendees.add(person)

    return redirect(to='meeting_detail', model_id=model_id)
