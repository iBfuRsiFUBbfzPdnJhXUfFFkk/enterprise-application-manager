from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.action import Action


class ActionForm(BaseModelForm):
    class Meta(BaseModelFormMeta):
        model = Action
