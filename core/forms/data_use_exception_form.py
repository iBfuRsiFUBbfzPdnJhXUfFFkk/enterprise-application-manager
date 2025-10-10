from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.data_use_exception import DataUseException


class DataUseExceptionForm(BaseModelForm):
    class Meta(BaseModelFormMeta):
        model = DataUseException
