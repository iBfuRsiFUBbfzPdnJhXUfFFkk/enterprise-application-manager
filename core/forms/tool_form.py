from django.forms import CheckboxSelectMultiple, ModelMultipleChoiceField

from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.service_provider import ServiceProvider
from core.models.tool import Tool


class ToolForm(BaseModelForm):
    service_providers = ModelMultipleChoiceField(
        queryset=ServiceProvider.objects.all(),
        widget=CheckboxSelectMultiple(),
        required=False,
        label='Service Providers'
    )

    class Meta(BaseModelFormMeta):
        model = Tool

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['service_providers'].initial = self.instance.service_providers.all()

    def save(self, commit=True):
        instance = super().save(commit=commit)
        if commit:
            instance.service_providers.set(self.cleaned_data['service_providers'])
        return instance
