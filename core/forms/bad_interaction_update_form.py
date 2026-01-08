from django.forms import FileField, Textarea

from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.bad_interaction_update import BadInteractionUpdate


class BadInteractionUpdateForm(BaseModelForm):
    attachment = FileField(required=False, help_text='Attach a file to this update (optional)')

    class Meta(BaseModelFormMeta):
        model = BadInteractionUpdate
        fields = ['comment']
        widgets = {
            'comment': Textarea(attrs={'rows': 3, 'placeholder': 'Add an update or note...'}),
        }
