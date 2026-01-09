from typing import Any, Mapping

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect

from core.forms.meeting_action_item_form import MeetingActionItemForm
from core.models.meeting_action_item import MeetingActionItem
from core.utilities.base_render import base_render


def meeting_action_item_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    """Edit an existing action item."""
    action_item = get_object_or_404(MeetingActionItem, pk=model_id)

    if request.method == 'POST':
        form = MeetingActionItemForm(request.POST, instance=action_item)
        if form.is_valid():
            form.save()
            return redirect(to='meeting_action_item_detail', model_id=action_item.id)
    else:
        form = MeetingActionItemForm(instance=action_item)

    context: Mapping[str, Any] = {'form': form, 'action_item': action_item}
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/meeting_action_item/meeting_action_item_form.html',
    )
