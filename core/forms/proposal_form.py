from django.forms import DateInput, ModelMultipleChoiceField, SelectMultiple

from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.proposal import Proposal
from core.models.link import Link


class ProposalForm(BaseModelForm):
    links = ModelMultipleChoiceField(
        queryset=Link.objects.all(),
        required=False,
        widget=SelectMultiple()
    )

    class Meta(BaseModelFormMeta):
        model = Proposal
        widgets = {
            "date_created": DateInput(attrs={"type": "date"}),
            "date_submitted": DateInput(attrs={"type": "date"}),
            "date_review_completed": DateInput(attrs={"type": "date"}),
            "date_decision": DateInput(attrs={"type": "date"}),
            "date_implementation_target": DateInput(attrs={"type": "date"}),
        }
