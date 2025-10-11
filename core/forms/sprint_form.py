from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.sprint import Sprint


class SprintForm(BaseModelForm):
    class Meta(BaseModelFormMeta):
        model = Sprint
