from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.external_blockers import ExternalBlockers


class ExternalBlockerForm(BaseModelForm):
    class Meta(BaseModelFormMeta):
        model = ExternalBlockers
