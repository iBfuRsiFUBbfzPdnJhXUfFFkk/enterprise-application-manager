from django import forms

from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.link import Link
from core.utilities.generate_short_code import validate_short_code


class LinkForm(BaseModelForm):
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
