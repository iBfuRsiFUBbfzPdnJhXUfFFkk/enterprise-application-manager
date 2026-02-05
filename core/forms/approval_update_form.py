from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.approval_update import ApprovalUpdate


class ApprovalUpdateForm(BaseModelForm):
    class Meta(BaseModelFormMeta):
        model = ApprovalUpdate
        fields = ['comment', 'is_internal_note']
