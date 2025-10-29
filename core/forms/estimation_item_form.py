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
            # Default all hour fields to 0
            hour_fields = [
                'hours_junior', 'hours_mid', 'hours_senior', 'hours_lead',
                'code_review_hours_junior', 'code_review_hours_mid', 'code_review_hours_senior', 'code_review_hours_lead',
                'code_reviewer_hours',
                'tests_hours_junior', 'tests_hours_mid', 'tests_hours_senior', 'tests_hours_lead'
            ]
            for field in hour_fields:
                if field not in self.initial:
                    self.initial[field] = 0.0

            # Default cone of uncertainty to requirements complete (middle ground)
            if 'cone_of_uncertainty' not in self.initial:
                self.initial['cone_of_uncertainty'] = 'REQUIREMENTS_COMPLETE'

            # Default complexity to medium
            if 'complexity_level' not in self.initial:
                self.initial['complexity_level'] = 'MEDIUM'

            # Priority defaults to N/A (None)
            # No default set - field remains empty
