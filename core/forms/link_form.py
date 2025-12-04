from django import forms
from django.forms import ModelMultipleChoiceField, SelectMultiple

from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.application import Application
from core.models.link import Link
from core.utilities.generate_short_code import validate_short_code


class LinkForm(BaseModelForm):
    applications = ModelMultipleChoiceField(
        queryset=Application.objects.all(),
        required=False,
        widget=SelectMultiple(attrs={'class': 'select2-applications'})
    )

    class Meta(BaseModelFormMeta):
        model = Link
        fields = ['name', 'url', 'comment', 'short_code', 'is_short_url_active']
        widgets = {
            'short_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Leave blank to auto-generate (e.g., abc123xyz0)',
                'maxlength': '50',
            }),
            'is_short_url_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make is_short_url_active not required so modal can omit it
        # It will use the model default (True) when not provided
        self.fields['is_short_url_active'].required = False
        # Set initial value to True for new instances
        if not self.instance.pk:
            self.fields['is_short_url_active'].initial = True

        # Populate reverse M2M relationships for editing
        if self.instance and self.instance.pk:
            self.fields['applications'].initial = self.instance.applications.all()

    def clean_is_short_url_active(self):
        """
        Default to True if not provided (e.g., from modal).
        When the modal doesn't send this field, it defaults to False,
        but we want new links to be active by default.
        """
        is_active = self.cleaned_data.get('is_short_url_active')

        # For new instances, default to True if not explicitly set
        if not self.instance.pk:
            # Check if the field was actually in the original data
            # If 'is_short_url_active' key doesn't exist in data, default to True
            if 'is_short_url_active' not in self.data:
                return True

        return is_active

    def clean_short_code(self):
        """Validate the short code if provided by user."""
        short_code = self.cleaned_data.get('short_code')

        # If empty, it will be auto-generated in model's save()
        if not short_code:
            return short_code

        # Validate format
        is_valid, error_message = validate_short_code(short_code)
        if not is_valid:
            raise forms.ValidationError(error_message)

        # Check uniqueness (excluding current instance if editing)
        existing_link = Link.objects.filter(short_code__iexact=short_code)
        if self.instance and self.instance.pk:
            existing_link = existing_link.exclude(pk=self.instance.pk)

        if existing_link.exists():
            raise forms.ValidationError(f'Short code "{short_code}" is already in use.')

        return short_code

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()
            self.save_m2m()

        # Save reverse M2M relationships
        if self.instance.pk and 'applications' in self.cleaned_data:
            self.instance.applications.set(self.cleaned_data['applications'])

        return instance
