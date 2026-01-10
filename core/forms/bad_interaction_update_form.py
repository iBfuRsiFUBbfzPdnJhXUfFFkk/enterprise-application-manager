from django.forms import Textarea

from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.bad_interaction_update import BadInteractionUpdate


class BadInteractionUpdateForm(BaseModelForm):
    class Meta(BaseModelFormMeta):
        model = BadInteractionUpdate
        fields = ['comment', 'attachment_file']
        widgets = {
            'comment': Textarea(attrs={'rows': 3, 'placeholder': 'Add an update or note...'}),
        }
