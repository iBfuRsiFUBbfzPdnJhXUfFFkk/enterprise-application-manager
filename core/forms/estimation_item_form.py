from django import forms
from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.estimation_item import EstimationItem


class EstimationItemForm(BaseModelForm):
    class Meta(BaseModelFormMeta):
        model = EstimationItem
        exclude = ['enumeration_attack_uuid', 'order', 'estimation']
        widgets = {
            'group': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Frontend, Backend, Database (optional)',
                'list': 'group-datalist'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Get existing group names from the estimation for autocomplete
        estimation = None
        if self.instance and self.instance.pk:
            estimation = self.instance.estimation
        elif 'initial' in kwargs and 'estimation' in kwargs['initial']:
            estimation = kwargs['initial']['estimation']

        if estimation:
            # Get distinct group names from all items in this estimation
            existing_groups = EstimationItem.objects.filter(
                estimation=estimation
            ).exclude(
                group__isnull=True
            ).exclude(
                group=''
            ).values_list('group', flat=True).distinct().order_by('group')

            # Store existing groups for use in template via widget attrs
            self.fields['group'].widget.attrs['data-existing-groups'] = '|'.join(existing_groups)

        # Remove step validation to allow any decimal value (e.g., 0.63 hours is acceptable)
        hour_fields = [
            'hours_junior', 'hours_mid', 'hours_senior', 'hours_lead',
            'code_review_hours_junior', 'code_review_hours_mid', 'code_review_hours_senior', 'code_review_hours_lead',
            'code_reviewer_hours',
            'tests_hours_junior', 'tests_hours_mid', 'tests_hours_senior', 'tests_hours_lead'
        ]

        # Set step="any" on hour fields and story_points to allow any decimal value
        for field in hour_fields:
            if field in self.fields:
                self.fields[field].widget.attrs['step'] = 'any'

        if 'story_points' in self.fields:
            self.fields['story_points'].widget.attrs['step'] = 'any'

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
