from typing import Any, Mapping

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.meeting_action_item_form import MeetingActionItemForm
from core.utilities.base_render import base_render


def meeting_action_item_add_view(request: HttpRequest) -> HttpResponse:
    """Create a new action item."""
    if request.method == 'POST':
        form = MeetingActionItemForm(request.POST)
        if form.is_valid():
            action_item = form.save()
            return redirect(to='meeting_action_item_detail', model_id=action_item.id)
    else:
        form = MeetingActionItemForm()

    context: Mapping[str, Any] = {'form': form}
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/meeting_action_item/meeting_action_item_form.html',
    )
