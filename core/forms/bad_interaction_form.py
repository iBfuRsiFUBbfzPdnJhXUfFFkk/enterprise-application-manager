from django.forms import DateInput, Textarea

from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.bad_interaction import BadInteraction


class BadInteractionForm(BaseModelForm):
    class Meta(BaseModelFormMeta):
        model = BadInteraction
        fields = ['person', 'reported_by', 'date_occurred', 'description', 'comment', 'severity', 'evidence_file']
        widgets = {
            'date_occurred': DateInput(attrs={'type': 'date'}),
            'description': Textarea(attrs={'rows': 4}),
            'comment': Textarea(attrs={'rows': 3}),
        }
