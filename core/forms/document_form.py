from django.forms import FileField

from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.document import Document


class DocumentForm(BaseModelForm):
    blob_data = FileField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make blob_data required only for new documents (not editing)
        if not self.instance.pk:
            self.fields['blob_data'].required = True

    class Meta(BaseModelFormMeta):
        model = Document
