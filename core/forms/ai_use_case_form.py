from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.ai_use_case import AIUseCase


class AIUseCaseForm(BaseModelForm):
    class Meta(BaseModelFormMeta):
        model = AIUseCase
