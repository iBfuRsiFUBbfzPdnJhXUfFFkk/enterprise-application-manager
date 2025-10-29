from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.estimation_item import EstimationItem


class EstimationItemForm(BaseModelForm):
    class Meta(BaseModelFormMeta):
        model = EstimationItem
        exclude = ['enumeration_attack_uuid', 'order', 'estimation']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Configure hour fields to only allow 0.25 increments and no negative values
        hour_fields = [
            'hours_junior', 'hours_mid', 'hours_senior', 'hours_lead',
            'code_review_hours_junior', 'code_review_hours_mid', 'code_review_hours_senior', 'code_review_hours_lead',
            'code_reviewer_hours',
            'tests_hours_junior', 'tests_hours_mid', 'tests_hours_senior', 'tests_hours_lead'
        ]
        for field in hour_fields:
            if field in self.fields:
                self.fields[field].widget.attrs.update({
                    'step': '0.25',
                    'min': '0'
                })

        # Also apply to story_points
        if 'story_points' in self.fields:
            self.fields['story_points'].widget.attrs.update({
                'step': '0.25',
                'min': '0'
            })

        # Set default values if creating new item
        if not self.instance.pk:
            # Default all hour fields to 0
            for field in hour_fields:
                if field not in self.initial:
                    self.initial[field] = 0.0

            # Default story points to 0
            if 'story_points' not in self.initial:
                self.initial['story_points'] = 0.0

            # Default cone of uncertainty to requirements complete (middle ground)
            if 'cone_of_uncertainty' not in self.initial:
                self.initial['cone_of_uncertainty'] = 'REQUIREMENTS_COMPLETE'

            # Default complexity to medium
            if 'complexity_level' not in self.initial:
                self.initial['complexity_level'] = 'MEDIUM'

            # Priority defaults to N/A (None)
            # No default set - field remains empty
