from django.forms import DateTimeInput, ModelMultipleChoiceField, SelectMultiple, Textarea

from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.application import Application
from core.models.maintenance_window import MaintenanceWindow


class MaintenanceWindowForm(BaseModelForm):
    applications_affected = ModelMultipleChoiceField(
        queryset=Application.objects.all(),
        required=False,
        widget=SelectMultiple()
    )

    class Meta(BaseModelFormMeta):
        model = MaintenanceWindow
        fields = [
            'name',
            'description',
            'date_time_start',
            'date_time_end',
            'severity',
            'status',
            'person_contact',
            'person_created_by',
            'applications_affected',
            'comment',
        ]
        widgets = {
            'date_time_start': DateTimeInput(attrs={'type': 'datetime-local'}),
            'date_time_end': DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': Textarea(attrs={'rows': 4}),
            'comment': Textarea(attrs={'rows': 3}),
        }
