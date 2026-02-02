from typing import Any, Mapping

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.meeting_form import MeetingForm
from core.utilities.base_render import base_render


def meeting_add_view(request: HttpRequest) -> HttpResponse:
    """Create a new meeting."""
    current_user_person = getattr(request.user, 'person_mapping', None)

    if request.method == 'POST':
        form = MeetingForm(request.POST)
        if form.is_valid():
            meeting = form.save()

            # Auto-add organizer and current user to attendees
            people_to_add = set()
            if meeting.organizer:
                people_to_add.add(meeting.organizer)
            if current_user_person:
                people_to_add.add(current_user_person)

            for person in people_to_add:
                if not meeting.attendees.filter(pk=person.pk).exists():
                    meeting.attendees.add(person)

            return redirect(to='meeting_detail', model_id=meeting.id)
    else:
        # Pre-select current user as organizer if they have a Person mapping
        initial = {}
        if current_user_person:
            initial['organizer'] = current_user_person.pk
            initial['attendees'] = [current_user_person.pk]
        form = MeetingForm(initial=initial)

    context: Mapping[str, Any] = {'form': form}
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/meeting/meeting_form.html',
    )
