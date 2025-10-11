from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.risk import Risk


class RiskForm(BaseModelForm):
    class Meta(BaseModelFormMeta):
        model = Risk
