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
            }),
            'links': forms.SelectMultiple(attrs={
                'class': 'form-control',
                'id': 'id_links',
                'size': '1'  # Will be enhanced with JavaScript
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

        # Configure hour fields with min=0 and step=any for precise decimal values
        hour_fields = [
            'hours_junior', 'hours_mid', 'hours_senior', 'hours_lead',
            'code_review_hours_junior', 'code_review_hours_mid', 'code_review_hours_senior', 'code_review_hours_lead',
            'code_reviewer_hours',
            'tests_hours_junior', 'tests_hours_mid', 'tests_hours_senior', 'tests_hours_lead'
        ]

        # Set min=0 and step=any on hour fields to allow precise decimal values
        for field in hour_fields:
            if field in self.fields:
                self.fields[field].widget.attrs['min'] = '0'
                self.fields[field].widget.attrs['step'] = 'any'

        if 'story_points' in self.fields:
            self.fields['story_points'].widget.attrs['step'] = 'any'

        # Format existing hour values to 2 decimal places for display in input fields
        if self.instance.pk:
            for field in hour_fields:
                if field in self.fields:
                    value = getattr(self.instance, field, None)
                    if value is not None:
                        # Format to 2 decimal places
                        self.initial[field] = f"{float(value):.2f}"

            # Also format story_points
            if 'story_points' in self.fields and self.instance.story_points is not None:
                self.initial['story_points'] = f"{float(self.instance.story_points):.2f}"

        # Set default values if creating new item
        if not self.instance.pk:
            # Default lead dev hours to 1.00
            if 'hours_lead' not in self.initial:
                self.initial['hours_lead'] = "1.00"

            # Calculate other development hours based on lead dev hours (1.00)
            # Senior = 1.25x, Mid = 2x, Junior = 3x
            if 'hours_senior' not in self.initial:
                self.initial['hours_senior'] = "1.25"
            if 'hours_mid' not in self.initial:
                self.initial['hours_mid'] = "2.00"
            if 'hours_junior' not in self.initial:
                self.initial['hours_junior'] = "3.00"

            # Calculate code review hours (0.5x of dev hours)
            if 'code_review_hours_lead' not in self.initial:
                self.initial['code_review_hours_lead'] = "0.50"
            if 'code_review_hours_senior' not in self.initial:
                self.initial['code_review_hours_senior'] = "0.62"  # 1.25 * 0.5
            if 'code_review_hours_mid' not in self.initial:
                self.initial['code_review_hours_mid'] = "1.00"  # 2.00 * 0.5
            if 'code_review_hours_junior' not in self.initial:
                self.initial['code_review_hours_junior'] = "1.50"  # 3.00 * 0.5

            # Calculate code reviewer hours (1x of lead code review)
            if 'code_reviewer_hours' not in self.initial:
                self.initial['code_reviewer_hours'] = "0.50"  # 1x of 0.50

            # Calculate testing hours (1x of dev hours)
            if 'tests_hours_lead' not in self.initial:
                self.initial['tests_hours_lead'] = "1.00"
            if 'tests_hours_senior' not in self.initial:
                self.initial['tests_hours_senior'] = "1.25"
            if 'tests_hours_mid' not in self.initial:
                self.initial['tests_hours_mid'] = "2.00"
            if 'tests_hours_junior' not in self.initial:
                self.initial['tests_hours_junior'] = "3.00"

            # Default story points to 1
            if 'story_points' not in self.initial:
                self.initial['story_points'] = "1"

            # Default cone of uncertainty to requirements complete (middle ground)
            if 'cone_of_uncertainty' not in self.initial:
                self.initial['cone_of_uncertainty'] = 'REQUIREMENTS_COMPLETE'

            # Complexity defaults to None - user must select
            # No default set - field remains empty

            # Priority defaults to None - user must select
            # No default set - field remains empty
