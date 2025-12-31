from django.forms import FileField

from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.forms.common.generic_multiple_choice_field import generic_multiple_choice_field
from core.models.application import Application
from core.models.document import Document


class DocumentForm(BaseModelForm):
    blob_data = FileField(required=False)
    applications = generic_multiple_choice_field(queryset=Application.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make blob_data required only for new documents (not editing)
        if not self.instance.pk:
            self.fields['blob_data'].required = True

    class Meta(BaseModelFormMeta):
        model = Document
