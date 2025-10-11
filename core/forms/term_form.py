from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.term import Term


class TermForm(BaseModelForm):
    class Meta(BaseModelFormMeta):
        model = Term
