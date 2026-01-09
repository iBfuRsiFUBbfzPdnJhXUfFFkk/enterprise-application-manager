from typing import Any, Mapping

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404

from core.models.meeting_action_item import MeetingActionItem
from core.utilities.base_render import base_render


def meeting_action_item_detail_view(request: HttpRequest, model_id: int) -> HttpResponse:
    """Detail view for an action item."""
    action_item = get_object_or_404(
        MeetingActionItem.objects.select_related('meeting', 'assignee'), pk=model_id
    )

    context: Mapping[str, Any] = {
        'action_item': action_item,
    }
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/meeting_action_item/meeting_action_item_detail.html',
    )
