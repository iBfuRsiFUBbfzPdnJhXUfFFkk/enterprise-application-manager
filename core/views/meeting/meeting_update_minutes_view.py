from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect

from core.models.meeting import Meeting


def meeting_update_minutes_view(request: HttpRequest, model_id: int) -> HttpResponse:
    """Update meeting minutes from the detail page."""
    meeting = get_object_or_404(Meeting, pk=model_id)

    if request.method == 'POST':
        minutes = request.POST.get('minutes', '')
        meeting.minutes = minutes
        meeting.save()

    return redirect(to='meeting_detail', model_id=model_id)
