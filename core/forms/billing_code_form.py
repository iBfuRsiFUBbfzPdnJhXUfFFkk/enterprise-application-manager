from django.forms import SelectMultiple

from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.forms.common.generic_person_choice_field import generic_person_choice_field
from core.models.billing_code import BillingCode
from core.models.project import Project
from core.models.team import Team


class BillingCodeForm(BaseModelForm):
    project_manager = generic_person_choice_field(is_project_manager=True)

    class Meta(BaseModelFormMeta):
        model = BillingCode

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Customize projects field display and add Select2
        if 'projects' in self.fields:
            self.fields['projects'].queryset = Project.objects.all().order_by('name')
            self.fields['projects'].label_from_instance = lambda obj: obj.name
            self.fields['projects'].widget = SelectMultiple(attrs={'class': 'select2-projects'})
            self.fields['projects'].widget.choices = self.fields['projects'].choices

        # Customize replaces field - exclude self and show all codes
        if 'replaces' in self.fields:
            queryset = BillingCode.objects.all().order_by('-is_active', 'name')
            # Exclude self if editing an existing billing code
            if self.instance and self.instance.pk:
                queryset = queryset.exclude(pk=self.instance.pk)
            self.fields['replaces'].queryset = queryset
            self.fields['replaces'].label_from_instance = lambda obj: f"{obj.name} - {obj.billing_code} {'(Active)' if obj.is_active else '(Retired)'}"
            self.fields['replaces'].required = False

        # Customize team field display
        if 'team' in self.fields:
            self.fields['team'].queryset = Team.objects.all().order_by('name')
            self.fields['team'].label_from_instance = lambda obj: obj.name
