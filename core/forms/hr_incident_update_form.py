from django.forms import Textarea

from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.forms.common.generic_multiple_choice_field import generic_multiple_choice_field
from core.models.document import Document
from core.models.hr_incident_update import HRIncidentUpdate


class HRIncidentUpdateForm(BaseModelForm):
    documents = generic_multiple_choice_field(queryset=Document.objects.all())

    class Meta(BaseModelFormMeta):
        model = HRIncidentUpdate
        fields = ['comment', 'attachment_file', 'documents']
        widgets = {
            'comment': Textarea(attrs={'rows': 3, 'placeholder': 'Add an update or note...'}),
        }
