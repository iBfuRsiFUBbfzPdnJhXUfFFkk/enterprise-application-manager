from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.team import Team


class TeamForm(BaseModelForm):
    class Meta(BaseModelFormMeta):
        model = Team
