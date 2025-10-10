from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.data_point import DataPoint


class DataPointForm(BaseModelForm):
    class Meta(BaseModelFormMeta):
        model = DataPoint
