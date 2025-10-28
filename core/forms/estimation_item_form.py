from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.estimation_item import EstimationItem


class EstimationItemForm(BaseModelForm):
    class Meta(BaseModelFormMeta):
        model = EstimationItem

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set default values if creating new item
        if not self.instance.pk:
            # Default hours to 0
            for field in ['hours_junior', 'hours_mid', 'hours_senior', 'hours_lead']:
                if field not in self.initial:
                    self.initial[field] = 0.0

            # Default cone of uncertainty to requirements complete (middle ground)
            if 'cone_of_uncertainty' not in self.initial:
                self.initial['cone_of_uncertainty'] = 'REQUIREMENTS_COMPLETE'

            # Default complexity to medium
            if 'complexity_level' not in self.initial:
                self.initial['complexity_level'] = 'MEDIUM'

            # Default priority to medium
            if 'priority' not in self.initial:
                self.initial['priority'] = 'MEDIUM'
