from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.api import API


class APIForm(BaseModelForm):
    class Meta(BaseModelFormMeta):
        model = API
