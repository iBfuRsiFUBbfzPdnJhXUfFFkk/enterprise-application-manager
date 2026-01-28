from django import forms
from django.forms import Textarea

from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.hr_incident_update import HRIncidentUpdate


class HRIncidentUpdateForm(BaseModelForm):
    # File upload field (not a model field - handled by view to create Document)
    attachment_upload = forms.FileField(
        required=False,
        help_text='Attachment file stored in MinIO object storage'
    )

    class Meta(BaseModelFormMeta):
        model = HRIncidentUpdate
        fields = ['comment']
        widgets = {
            'comment': Textarea(attrs={'rows': 3, 'placeholder': 'Add an update or note...'}),
        }
