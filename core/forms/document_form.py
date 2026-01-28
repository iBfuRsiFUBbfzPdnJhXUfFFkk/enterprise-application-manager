from django.forms import ModelMultipleChoiceField, SelectMultiple

from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.application import Application
from core.models.document import Document


class DocumentForm(BaseModelForm):
    applications = ModelMultipleChoiceField(
        queryset=Application.objects.all().order_by('name'),
        required=False,
        widget=SelectMultiple(attrs={'class': 'searchable-multi-select'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make file required only for new documents (not editing)
        if not self.instance.pk:
            self.fields['file'].required = True
            self.fields['version'].initial = 1
        else:
            # Populate applications from reverse relation for existing documents
            self.fields['applications'].initial = self.instance.applications.all()

    def save(self, commit=True):
        document = super().save(commit=commit)
        if commit:
            # Update the reverse ManyToMany relation
            selected_apps = self.cleaned_data.get('applications', [])
            # Get current applications that have this document
            current_apps = set(document.applications.all())
            selected_apps_set = set(selected_apps)

            # Remove document from apps that are no longer selected
            for app in current_apps - selected_apps_set:
                app.documents.remove(document)

            # Add document to newly selected apps
            for app in selected_apps_set - current_apps:
                app.documents.add(document)

        return document

    class Meta(BaseModelFormMeta):
        model = Document
        fields = ['name', 'version', 'comment', 'file']
