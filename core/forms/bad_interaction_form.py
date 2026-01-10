from django.forms import DateInput, Textarea

from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.forms.common.generic_multiple_choice_field import generic_multiple_choice_field
from core.models.bad_interaction import BadInteraction
from core.models.document import Document


class BadInteractionForm(BaseModelForm):
    documents = generic_multiple_choice_field(queryset=Document.objects.all())

    class Meta(BaseModelFormMeta):
        model = BadInteraction
        fields = ['person', 'reported_by', 'date_occurred', 'description', 'comment', 'severity', 'evidence_file', 'documents']
        widgets = {
            'date_occurred': DateInput(attrs={'type': 'date'}),
            'description': Textarea(attrs={'rows': 4}),
            'comment': Textarea(attrs={'rows': 3}),
        }
