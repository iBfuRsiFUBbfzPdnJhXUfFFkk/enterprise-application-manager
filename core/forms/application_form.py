from typing import cast

from django.db.models import QuerySet
from django.forms import ModelForm, DateField, DateInput, ModelMultipleChoiceField, CheckboxSelectMultiple

from core.models.application import Application
from core.models.person import Person


class ApplicationForm(ModelForm):
    date_launch = DateField(
        widget=DateInput(attrs={'type': 'date'}),
    )
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
