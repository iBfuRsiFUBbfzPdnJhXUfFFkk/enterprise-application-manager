from django.forms import DateInput, FileField, Textarea

from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.bad_interaction import BadInteraction


class BadInteractionForm(BaseModelForm):
    evidence = FileField(required=False, help_text='Upload evidence file (PDF, image, document)')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make evidence required only for new bad interactions (not editing)
        if not self.instance.pk:
            self.fields['evidence'].required = False

    class Meta(BaseModelFormMeta):
        model = BadInteraction
        fields = ['person', 'reported_by', 'date_occurred', 'description', 'comment', 'severity']
        widgets = {
            'date_occurred': DateInput(attrs={'type': 'date'}),
            'description': Textarea(attrs={'rows': 4}),
            'comment': Textarea(attrs={'rows': 3}),
        }
