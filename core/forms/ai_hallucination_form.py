from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.ai_hallucination import AIHallucination


class AIHallucinationForm(BaseModelForm):
    class Meta(BaseModelFormMeta):
        model = AIHallucination
