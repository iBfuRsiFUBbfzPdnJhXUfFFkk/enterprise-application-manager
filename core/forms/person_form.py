from django.forms import ModelMultipleChoiceField, SelectMultiple

from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.forms.common.generic_choice_field import generic_choice_field
from core.forms.common.generic_date_field import generic_date_field
from core.forms.common.generic_multiple_choice_field import generic_multiple_choice_field
from core.models.application import Application
from core.models.job_level import JobLevel
from core.models.job_title import JobTitle
from core.models.person import Person
from core.models.role import Role
from core.models.skill import Skill


class PersonForm(BaseModelForm):
    # Use SelectMultiple widget for applications fields (for searchable chip selector component)
    applications_developer_of = ModelMultipleChoiceField(
        queryset=Application.objects.all(),
        required=False,
        widget=SelectMultiple(attrs={'class': 'searchable-multi-select'})
    )
    applications_stakeholder_of = ModelMultipleChoiceField(
        queryset=Application.objects.all(),
        required=False,
        widget=SelectMultiple(attrs={'class': 'searchable-multi-select'})
    )
    date_birthday = generic_date_field()
    date_hired = generic_date_field()
    date_left = generic_date_field()
    job_level = generic_choice_field(queryset=JobLevel.objects.all())
    job_title = generic_choice_field(queryset=JobTitle.objects.all())
    roles = generic_multiple_choice_field(queryset=Role.objects.all())
    skills = generic_multiple_choice_field(queryset=Skill.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Populate reverse M2M relationships for editing
        if self.instance and self.instance.pk:
            # Load existing applications where this person is a developer
            self.fields['applications_developer_of'].initial = self.instance.applications_developer_of.all()
            # Load existing applications where this person is a stakeholder
            self.fields['applications_stakeholder_of'].initial = self.instance.applications_stakeholder_of.all()

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()
            # Save standard M2M relationships (roles, skills, etc.)
            self.save_m2m()

        # Save reverse M2M relationships
        if self.instance.pk:
            # Clear and set developer applications
            if 'applications_developer_of' in self.cleaned_data:
                self.instance.applications_developer_of.set(self.cleaned_data['applications_developer_of'])

            # Clear and set stakeholder applications
            if 'applications_stakeholder_of' in self.cleaned_data:
                self.instance.applications_stakeholder_of.set(self.cleaned_data['applications_stakeholder_of'])

        return instance

    class Meta(BaseModelFormMeta):
        model = Person
