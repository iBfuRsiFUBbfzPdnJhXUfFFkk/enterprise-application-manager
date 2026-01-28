from django import forms
from django.forms import DateInput, Textarea

from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.bad_interaction import BadInteraction


class BadInteractionForm(BaseModelForm):
    # File upload field (not a model field - handled by view to create Document)
    evidence_upload = forms.FileField(
        required=False,
        help_text='Evidence file stored in MinIO object storage'
    )

    class Meta(BaseModelFormMeta):
        model = BadInteraction
        fields = ['name', 'person', 'reported_by', 'date_occurred', 'description', 'comment', 'severity']
        widgets = {
            'date_occurred': DateInput(attrs={'type': 'date'}),
            'description': Textarea(attrs={'rows': 4}),
            'comment': Textarea(attrs={'rows': 3}),
        }
