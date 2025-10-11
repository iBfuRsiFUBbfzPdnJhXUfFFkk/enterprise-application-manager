from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.onboard_procedure import OnboardProcedure


class OnboardProcedureForm(BaseModelForm):
    class Meta(BaseModelFormMeta):
        model = OnboardProcedure
