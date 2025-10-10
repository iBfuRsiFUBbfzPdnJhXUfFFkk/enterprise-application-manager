from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.hotfix import Hotfix


class HotfixForm(BaseModelForm):
    class Meta(BaseModelFormMeta):
        model = Hotfix
