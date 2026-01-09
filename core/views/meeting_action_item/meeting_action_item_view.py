from django.http import HttpRequest, HttpResponse

from core.models.meeting_action_item import MeetingActionItem
from core.views.generic.generic_view import generic_view


def meeting_action_item_view(request: HttpRequest) -> HttpResponse:
    """List view for action items with advanced filtering."""
    # Get filter parameters
    status_filter: str | None = request.GET.get('status')
    priority_filter: str | None = request.GET.get('priority')
    assignee_filter: str | None = request.GET.get('assignee')
    my_items: str | None = request.GET.get('my_items')

    # Start with base queryset
    queryset = MeetingActionItem.objects.all()

    # Apply filters
    if status_filter:
        queryset = queryset.filter(status=status_filter)
    if priority_filter:
        queryset = queryset.filter(priority=priority_filter)
    if assignee_filter:
        queryset = queryset.filter(assignee_id=assignee_filter)
    if my_items == 'true' and hasattr(request.user, 'person'):
        queryset = queryset.filter(assignee=request.user.person)

    return generic_view(
        model_cls=MeetingActionItem,
        name='meeting_action_item',
        request=request,
        queryset=queryset,
    )
