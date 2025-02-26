from django.forms import ModelForm, FileField

from core.models.document import Document


class DocumentForm(ModelForm):
    blob_data = FileField(required=False)

    class Meta:
        fields = ['name', 'version', 'comment']
        model = Document
