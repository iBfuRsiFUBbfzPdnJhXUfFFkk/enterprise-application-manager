from typing import cast

from django.db.models import QuerySet
from django.forms import ModelForm, ModelMultipleChoiceField, CheckboxSelectMultiple

from core.forms.common.generic_date_field import generic_date_field
from core.models.person import Person
from core.models.role import Role


class PersonForm(ModelForm):
    date_birthday = generic_date_field()
    date_hired = generic_date_field()
    date_left = generic_date_field()

    roles = ModelMultipleChoiceField(
        queryset=cast(QuerySet, Role.objects),
        required=False,
        widget=CheckboxSelectMultiple
    )

    class Meta:
        fields = '__all__'
        model = Person
