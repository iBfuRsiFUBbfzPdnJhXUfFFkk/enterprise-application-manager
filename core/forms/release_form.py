from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.release import Release


class ReleaseForm(BaseModelForm):
    class Meta(BaseModelFormMeta):
        model = Release
