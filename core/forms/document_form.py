from django.forms import FileField

from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.document import Document


class DocumentForm(BaseModelForm):
    blob_data = FileField(required=True)

    class Meta(BaseModelFormMeta):
        model = Document
