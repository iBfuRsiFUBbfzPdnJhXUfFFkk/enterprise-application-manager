from django.forms import Textarea

from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.comment import Comment


class CommentForm(BaseModelForm):
    """Form for creating and editing comments."""

    class Meta(BaseModelFormMeta):
        model = Comment
        fields = ['content', 'is_internal']
        widgets = {
            'content': Textarea(attrs={'rows': 4}),
        }
