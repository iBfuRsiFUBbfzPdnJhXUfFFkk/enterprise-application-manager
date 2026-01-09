from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect

from core.models.meeting_action_item import MeetingActionItem


def meeting_action_item_delete_view(request: HttpRequest, model_id: int) -> HttpResponse:
    """Delete an action item."""
    action_item = get_object_or_404(MeetingActionItem, pk=model_id)
    action_item.delete()
    return redirect(to='meeting_action_item')
