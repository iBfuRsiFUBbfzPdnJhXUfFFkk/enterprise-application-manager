from django.forms import Textarea

from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.meeting_note import MeetingNote


class MeetingNoteForm(BaseModelForm):
    """Form for adding notes and quotes during a meeting."""

    class Meta(BaseModelFormMeta):
        model = MeetingNote
        fields = ['note_type', 'person', 'content']
        widgets = {
            'content': Textarea(attrs={'rows': 3, 'placeholder': 'Add your note or quote here...'}),
        }
