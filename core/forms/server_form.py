from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.server import Server


class ServerForm(BaseModelForm):
    class Meta(BaseModelFormMeta):
        model = Server
