from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.estimation import Estimation


class EstimationForm(BaseModelForm):
    class Meta(BaseModelFormMeta):
        model = Estimation

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set default contingency padding if creating new estimation
        if not self.instance.pk and 'contingency_padding_percent' not in self.initial:
            self.initial['contingency_padding_percent'] = 20.0
