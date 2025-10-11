from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.policy import Policy


class PolicyForm(BaseModelForm):
    class Meta(BaseModelFormMeta):
        model = Policy
