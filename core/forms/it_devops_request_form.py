from django.forms import DateInput, ModelMultipleChoiceField, SelectMultiple

from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.it_devops_request import ITDevOpsRequest
from core.models.link import Link


class ITDevOpsRequestForm(BaseModelForm):
    links = ModelMultipleChoiceField(
        queryset=Link.objects.all(),
        required=False,
        widget=SelectMultiple()
    )

    class Meta(BaseModelFormMeta):
        model = ITDevOpsRequest
        widgets = {
            "date_requested": DateInput(attrs={"type": "date"}),
            "date_due": DateInput(attrs={"type": "date"}),
            "date_completed": DateInput(attrs={"type": "date"}),
        }
