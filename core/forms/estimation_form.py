from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.estimation import Estimation


class EstimationForm(BaseModelForm):
    class Meta(BaseModelFormMeta):
        model = Estimation

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Configure developer count fields to only allow positive integers
        count_fields = [
            'junior_developer_count',
            'mid_developer_count',
            'senior_developer_count',
            'lead_developer_count',
            'reviewer_count'
        ]
        for field in count_fields:
            if field in self.fields:
                self.fields[field].widget.attrs.update({
                    'min': '0',
                    'step': '1'
                })

        # Set default contingency padding if creating new estimation
        if not self.instance.pk and 'contingency_padding_percent' not in self.initial:
            self.initial['contingency_padding_percent'] = 20.0
