from typing import Any, Mapping

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.meeting_form import MeetingForm
from core.utilities.base_render import base_render


def meeting_add_view(request: HttpRequest) -> HttpResponse:
    """Create a new meeting."""
    if request.method == 'POST':
        form = MeetingForm(request.POST)
        if form.is_valid():
            meeting = form.save()
            return redirect(to='meeting_detail', model_id=meeting.id)
    else:
        form = MeetingForm()

    context: Mapping[str, Any] = {'form': form}
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/meeting/meeting_form.html',
    )
