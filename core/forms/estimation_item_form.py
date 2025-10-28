from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.estimation_item import EstimationItem


class EstimationItemForm(BaseModelForm):
    class Meta(BaseModelFormMeta):
        model = EstimationItem

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set default hours to 0 if creating new item
        if not self.instance.pk:
            for field in ['hours_junior', 'hours_mid', 'hours_senior', 'hours_lead']:
                if field not in self.initial:
                    self.initial[field] = 0.0
