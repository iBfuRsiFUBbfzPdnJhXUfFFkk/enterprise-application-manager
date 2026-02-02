from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect

from core.models.meeting import Meeting
from core.models.person import Person


def meeting_toggle_attendance_view(request: HttpRequest, model_id: int, person_id: int) -> HttpResponse:
    """Toggle a person's attendance status."""
    meeting = get_object_or_404(Meeting, pk=model_id)
    person = get_object_or_404(Person, pk=person_id)
    is_present = False

    if request.method == 'POST':
        if meeting.actual_attendees.filter(pk=person_id).exists():
            meeting.actual_attendees.remove(person)
            is_present = False
        else:
            meeting.actual_attendees.add(person)
            is_present = True

        # Return JSON for AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'is_present': is_present,
                'present_count': meeting.actual_attendees.count(),
            })

    return redirect(to='meeting_detail', model_id=model_id)
