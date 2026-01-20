from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.proposal_update import ProposalUpdate


class ProposalUpdateForm(BaseModelForm):
    class Meta(BaseModelFormMeta):
        model = ProposalUpdate
        fields = ["comment", "is_internal_note"]
