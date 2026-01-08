from django.forms import DateInput, Textarea

from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.forms.common.generic_multiple_choice_field import generic_multiple_choice_field
from core.models.bad_interaction import BadInteraction
from core.models.hr_incident import HRIncident


class HRIncidentForm(BaseModelForm):
    bad_interactions = generic_multiple_choice_field(queryset=BadInteraction.objects.all())

    class Meta(BaseModelFormMeta):
        model = HRIncident
        fields = ['reference_number', 'name', 'person', 'filed_by', 'date_filed', 'date_resolved', 'description', 'comment', 'status', 'resolution']
        widgets = {
            'date_filed': DateInput(attrs={'type': 'date'}),
            'date_resolved': DateInput(attrs={'type': 'date'}),
            'description': Textarea(attrs={'rows': 4}),
            'resolution': Textarea(attrs={'rows': 4}),
            'comment': Textarea(attrs={'rows': 3}),
        }
