from typing import Any

from django.forms import ModelMultipleChoiceField

from core.forms.common.generic_multiple_choice_field import generic_multiple_choice_field
from core.models.person import Person


def generic_person_multiple_choice_field(
        **kwargs: Any
) -> ModelMultipleChoiceField:
    return generic_multiple_choice_field(queryset=Person.objects.filter(**kwargs))
