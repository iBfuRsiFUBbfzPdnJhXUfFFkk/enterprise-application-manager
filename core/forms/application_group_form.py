from django.forms import ModelMultipleChoiceField, SelectMultiple
from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.application import Application
from core.models.application_group import ApplicationGroup


class ApplicationGroupForm(BaseModelForm):
    applications = ModelMultipleChoiceField(
        queryset=Application.objects.all().order_by('name'),
        required=False,
        widget=SelectMultiple(attrs={'class': 'searchable-multi-select', 'data-placeholder': 'Search and select applications...'})
    )

    class Meta(BaseModelFormMeta):
        model = ApplicationGroup

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If editing an existing group, set initial applications
        if self.instance and self.instance.pk:
            self.fields['applications'].initial = self.instance.applications.all()

    def save(self, commit=True):
        instance = super().save(commit=commit)
        if commit:
            # Get the selected applications
            applications = self.cleaned_data.get('applications', [])
            # Clear existing relationships where this group is the platform
            instance.applications.clear()
            # Set the new applications
            for app in applications:
                app.application_group_platform = instance
                app.save()
        return instance
