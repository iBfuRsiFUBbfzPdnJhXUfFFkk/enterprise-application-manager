from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.incident import Incident


class IncidentForm(BaseModelForm):
    class Meta(BaseModelFormMeta):
        model = Incident
