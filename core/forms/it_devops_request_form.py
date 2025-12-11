from django.forms import DateInput

from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.it_devops_request import ITDevOpsRequest


class ITDevOpsRequestForm(BaseModelForm):
    class Meta(BaseModelFormMeta):
        model = ITDevOpsRequest
        widgets = {
            "date_requested": DateInput(attrs={"type": "date"}),
            "date_due": DateInput(attrs={"type": "date"}),
            "date_completed": DateInput(attrs={"type": "date"}),
        }
