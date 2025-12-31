from django.forms import DateInput

from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.common.enums.task_status_choices import TASK_STATUS_TO_DO
from core.models.task import Task


class TaskForm(BaseModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set default status to "To Do" for new tasks
        if not self.instance.pk and 'status' in self.fields:
            self.fields['status'].initial = TASK_STATUS_TO_DO

    class Meta(BaseModelFormMeta):
        model = Task
        fields = ['name', 'priority', 'status', 'order', 'comment', 'date_completed']
        widgets = {
            'date_completed': DateInput(attrs={'type': 'date'}),
        }
        help_texts = {
            'date_completed': 'Leave blank unless manually setting completion date',
            'priority': 'Set task priority level',
            'status': 'Current status of the task',
            'order': 'Position in task list (lower numbers appear first)',
        }
