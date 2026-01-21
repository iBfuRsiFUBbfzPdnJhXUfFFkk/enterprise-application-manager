from django.forms import CheckboxSelectMultiple

from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.service_provider import ServiceProvider


class ServiceProviderForm(BaseModelForm):
    class Meta(BaseModelFormMeta):
        model = ServiceProvider
        widgets = {
            'tools': CheckboxSelectMultiple(),
        }
