from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.api_authentication import APIAuthentication


class APIAuthenticationForm(BaseModelForm):
    class Meta(BaseModelFormMeta):
        model = APIAuthentication
