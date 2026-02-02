from django.forms import DateTimeInput, SelectMultiple, Textarea

from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.meeting import Meeting
from core.models.person import Person


class MeetingForm(BaseModelForm):

    class Meta(BaseModelFormMeta):
        model = Meeting
        fields = [
            'name',
            'meeting_type',
            'status',
            'organizer',
            'datetime_start',
            'datetime_end',
            'attendees',
            'location_address',
            'location_address_continued',
            'location_city',
            'location_county',
            'location_state_code',
            'location_postal_code',
            'virtual_meeting_url',
            'description',
            'agenda',
            'minutes',
            'application',
            'project',
            'comment',
        ]
        widgets = {
            'datetime_start': DateTimeInput(attrs={'type': 'datetime-local'}),
            'datetime_end': DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': Textarea(attrs={'rows': 3}),
            'agenda': Textarea(attrs={'rows': 4}),
            'minutes': Textarea(attrs={'rows': 8}),
            'comment': Textarea(attrs={'rows': 2}),
            'attendees': SelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['attendees'].queryset = Person.objects.all().order_by(
            'name_last', 'name_first'
        )
        self.fields['organizer'].queryset = Person.objects.all().order_by(
            'name_last', 'name_first'
        )
