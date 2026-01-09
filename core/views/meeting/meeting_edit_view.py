from typing import Any, Mapping

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect

from core.forms.meeting_form import MeetingForm
from core.models.meeting import Meeting
from core.utilities.base_render import base_render


def meeting_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    """Edit an existing meeting."""
    meeting = get_object_or_404(Meeting, pk=model_id)

    if request.method == 'POST':
        form = MeetingForm(request.POST, instance=meeting)
        if form.is_valid():
            form.save()
            return redirect(to='meeting_detail', model_id=meeting.id)
    else:
        form = MeetingForm(instance=meeting)

    context: Mapping[str, Any] = {'form': form, 'meeting': meeting}
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/meeting/meeting_form.html',
    )
