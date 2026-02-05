from django.forms import DateInput, ModelMultipleChoiceField, SelectMultiple

from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.approval import Approval
from core.models.link import Link


class ApprovalForm(BaseModelForm):
    links = ModelMultipleChoiceField(
        queryset=Link.objects.all(),
        required=False,
        widget=SelectMultiple()
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.fields['status'].initial = 'pending'

    class Meta(BaseModelFormMeta):
        model = Approval
        widgets = {
            "date_requested": DateInput(attrs={"type": "date"}),
            "date_approved": DateInput(attrs={"type": "date"}),
            "date_expiration": DateInput(attrs={"type": "date"}),
        }
