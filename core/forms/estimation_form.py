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
            'lead_developer_count'
        ]
        for field in count_fields:
            if field in self.fields:
                self.fields[field].widget.attrs.update({
                    'min': '0',
                    'step': '1'
                })

        # Configure sprint duration field
        if 'sprint_duration_weeks' in self.fields:
            self.fields['sprint_duration_weeks'].widget.attrs.update({
                'min': '1',
                'step': '1'
            })

        # Set default contingency padding if creating new estimation
        if not self.instance.pk and 'contingency_padding_percent' not in self.initial:
            self.initial['contingency_padding_percent'] = 20.0

        # Configure story points modifier field to allow any decimal
        if 'story_points_modifier' in self.fields:
            self.fields['story_points_modifier'].widget.attrs.update({
                'step': 'any',
                'min': '0.01'
            })

        # Set default story points modifier if creating new estimation
        if not self.instance.pk and 'story_points_modifier' not in self.initial:
            self.initial['story_points_modifier'] = 1.0

        # Set default sprint duration if creating new estimation
        if not self.instance.pk and 'sprint_duration_weeks' not in self.initial:
            self.initial['sprint_duration_weeks'] = 3
