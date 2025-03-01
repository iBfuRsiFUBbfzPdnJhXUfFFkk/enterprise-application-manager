from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.acronym import Acronym


class AcronymForm(BaseModelForm):
    class Meta(BaseModelFormMeta):
        model = Acronym
