from typing import cast

from django.db.models import QuerySet
from django.forms import ModelForm, ModelMultipleChoiceField, CheckboxSelectMultiple

from core.forms.common.generic_date_field import generic_date_field
from core.models.application import Application
from core.models.person import Person


class ApplicationForm(ModelForm):
    date_launch = generic_date_field()
    person_developers = ModelMultipleChoiceField(
        queryset=cast(QuerySet, Person.objects.filter(is_developer=True)),
        widget=CheckboxSelectMultiple
    )
    person_stakeholders = ModelMultipleChoiceField(
        queryset=cast(QuerySet, Person.objects.filter(is_stakeholder=True)),
        widget=CheckboxSelectMultiple
    )

    class Meta:
        fields = '__all__'
        model = Application
