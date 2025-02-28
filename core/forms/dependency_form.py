from typing import cast

from django.db.models import QuerySet
from django.forms import ModelForm, ModelMultipleChoiceField, CheckboxSelectMultiple

from core.models.application import Application
from core.models.dependency import Dependency


class DependencyForm(ModelForm):
    applications = ModelMultipleChoiceField(
        queryset=cast(QuerySet, Application.objects),
        required=False,
        widget=CheckboxSelectMultiple
    )

    class Meta:
        fields = '__all__'
        model = Dependency
