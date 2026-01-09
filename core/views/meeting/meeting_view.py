from typing import Any, Mapping

from django.db.models import Q
from django.http import HttpRequest, HttpResponse

from core.models.meeting import Meeting
from core.utilities.base_render import base_render


def meeting_view(request: HttpRequest) -> HttpResponse:
    """List view for meetings with advanced filtering."""
    # Get filter parameters
    status_filter: str | None = request.GET.get('status')
    type_filter: str | None = request.GET.get('type')
    my_meetings: str | None = request.GET.get('my_meetings')

    # Start with base queryset
    queryset = Meeting.objects.all()

    # Apply filters
    if status_filter:
        queryset = queryset.filter(status=status_filter)
    if type_filter:
        queryset = queryset.filter(meeting_type=type_filter)
    if my_meetings == 'true' and hasattr(request.user, 'person'):
        queryset = queryset.filter(
            Q(organizer=request.user.person) | Q(attendees=request.user.person)
        ).distinct()

    context: Mapping[str, Any] = {
        'models': queryset,
    }
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/meeting/meeting.html',
    )
