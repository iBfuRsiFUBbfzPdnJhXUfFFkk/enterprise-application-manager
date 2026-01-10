from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.forms.common.generic_multiple_choice_field import generic_multiple_choice_field
from core.models.application import Application
from core.models.document import Document


class DocumentForm(BaseModelForm):
    applications = generic_multiple_choice_field(queryset=Application.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make file required only for new documents (not editing)
        if not self.instance.pk:
            self.fields['file'].required = True

    class Meta(BaseModelFormMeta):
        model = Document
        fields = ['name', 'version', 'comment', 'file']
