from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.application_group import ApplicationGroup


class ApplicationGroupForm(BaseModelForm):
    class Meta(BaseModelFormMeta):
        model = ApplicationGroup
