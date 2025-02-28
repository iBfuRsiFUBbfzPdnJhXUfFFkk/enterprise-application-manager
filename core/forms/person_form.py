from typing import cast

from django.db.models import QuerySet
from django.forms import ModelForm, ModelMultipleChoiceField, CheckboxSelectMultiple, ModelChoiceField

from core.forms.common.generic_date_field import generic_date_field
from core.models.job_level import JobLevel
from core.models.person import Person
from core.models.role import Role
from core.models.skill import Skill


class PersonForm(ModelForm):
    date_birthday = generic_date_field()
    date_hired = generic_date_field()
    date_left = generic_date_field()
    job_level = ModelChoiceField(
        queryset=cast(QuerySet, JobLevel.objects),
        required=False,
    )
    roles = ModelMultipleChoiceField(
        queryset=cast(QuerySet, Role.objects),
        required=False,
        widget=CheckboxSelectMultiple
    )
    skills = ModelMultipleChoiceField(
        queryset=cast(QuerySet, Skill.objects),
        required=False,
        widget=CheckboxSelectMultiple
    )

    class Meta:
        fields = '__all__'
        model = Person
