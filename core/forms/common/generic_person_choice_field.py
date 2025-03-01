from typing import Any

from django.forms import ModelChoiceField

from core.forms.common.generic_choice_field import generic_choice_field
from core.models.person import Person


def generic_person_choice_field(
        **kwargs: Any
) -> ModelChoiceField:
    return generic_choice_field(queryset=Person.objects.filter(**kwargs))
