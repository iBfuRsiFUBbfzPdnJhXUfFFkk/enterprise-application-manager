from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.role import Role


class RoleForm(BaseModelForm):
    class Meta(BaseModelFormMeta):
        model = Role
