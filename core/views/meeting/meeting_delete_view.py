from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect

from core.models.meeting import Meeting


def meeting_delete_view(request: HttpRequest, model_id: int) -> HttpResponse:
    """Delete a meeting."""
    meeting = get_object_or_404(Meeting, pk=model_id)
    meeting.delete()
    return redirect(to='meeting')
