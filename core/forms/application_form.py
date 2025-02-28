from typing import cast

from django.db.models import QuerySet
from django.forms import ModelForm, ModelMultipleChoiceField, CheckboxSelectMultiple, ModelChoiceField

from core.forms.common.generic_date_field import generic_date_field
from core.models.application import Application
from core.models.application_group import ApplicationGroup
from core.models.person import Person
from core.models.service_provider import ServiceProvider
from core.models.tool import Tool


class ApplicationForm(ModelForm):
    application_group_platform = ModelChoiceField(
        queryset=cast(QuerySet, ApplicationGroup.objects.filter(is_platform=True)),
        required=False,
    )
    application_groups = ModelMultipleChoiceField(
        queryset=cast(QuerySet, ApplicationGroup.objects),
        required=False,
        widget=CheckboxSelectMultiple
    )
    date_launch = generic_date_field()
    person_architect = ModelChoiceField(
        queryset=cast(QuerySet, Person.objects.filter(is_architect=True)),
        required=False,
    )
    person_developers = ModelMultipleChoiceField(
        queryset=cast(QuerySet, Person.objects.filter(is_developer=True)),
        required=False,
        widget=CheckboxSelectMultiple
    )
    person_lead_developer = ModelChoiceField(
        queryset=cast(QuerySet, Person.objects.filter(is_lead_developer=True)),
        required=False,
    )
    person_product_manager = ModelChoiceField(
        queryset=cast(QuerySet, Person.objects.filter(is_product_manager=True)),
        required=False,
    )
    person_product_owner = ModelChoiceField(
        queryset=cast(QuerySet, Person.objects.filter(is_product_owner=True)),
        required=False,
    )
    person_project_manager = ModelChoiceField(
        queryset=cast(QuerySet, Person.objects.filter(is_project_manager=True)),
        required=False,
    )
    person_scrum_master = ModelChoiceField(
        queryset=cast(QuerySet, Person.objects.filter(is_scrum_master=True)),
        required=False,
    )
    person_stakeholders = ModelMultipleChoiceField(
        queryset=cast(QuerySet, Person.objects.filter(is_stakeholder=True)),
        required=False,
        widget=CheckboxSelectMultiple
    )
    service_providers = ModelMultipleChoiceField(
        queryset=cast(QuerySet, ServiceProvider.objects),
        required=False,
        widget=CheckboxSelectMultiple
    )
    tools = ModelMultipleChoiceField(
        queryset=cast(QuerySet, Tool.objects),
        required=False,
        widget=CheckboxSelectMultiple
    )

    class Meta:
        fields = '__all__'
        model = Application
