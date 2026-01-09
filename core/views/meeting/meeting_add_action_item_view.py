from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect

from core.forms.meeting_action_item_form import MeetingActionItemInlineForm
from core.models.meeting import Meeting


def meeting_add_action_item_view(request: HttpRequest, model_id: int) -> HttpResponse:
    """Add an action item to a meeting from the detail page."""
    meeting = get_object_or_404(Meeting, pk=model_id)

    if request.method == 'POST':
        form = MeetingActionItemInlineForm(request.POST)
        if form.is_valid():
            action_item = form.save(commit=False)
            action_item.meeting = meeting
            action_item.status = 'open'  # Default status
            action_item.save()

    return redirect(to='meeting_detail', model_id=model_id)
