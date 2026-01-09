from django.forms import DateInput, Textarea

from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.meeting_action_item import MeetingActionItem


class MeetingActionItemForm(BaseModelForm):
    """Full form for creating/editing action items with all fields."""

    class Meta(BaseModelFormMeta):
        model = MeetingActionItem
        fields = [
            'name',
            'meeting',
            'assignee',
            'status',
            'priority',
            'due_date',
            'date_completed',
            'description',
            'comment',
        ]
        widgets = {
            'due_date': DateInput(attrs={'type': 'date'}),
            'date_completed': DateInput(attrs={'type': 'date'}),
            'description': Textarea(attrs={'rows': 3}),
            'comment': Textarea(attrs={'rows': 2}),
        }


class MeetingActionItemInlineForm(BaseModelForm):
    """Simplified form for adding action items from meeting detail page."""

    class Meta(BaseModelFormMeta):
        model = MeetingActionItem
        fields = ['name', 'assignee', 'priority', 'due_date', 'description']
        widgets = {
            'due_date': DateInput(attrs={'type': 'date'}),
            'description': Textarea(attrs={'rows': 2}),
        }
