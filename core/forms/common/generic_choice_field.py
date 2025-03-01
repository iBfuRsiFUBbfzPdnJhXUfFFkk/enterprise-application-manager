from django.db.models import QuerySet
from django.forms import ModelChoiceField


def generic_choice_field(
        queryset: QuerySet,
) -> ModelChoiceField:
    return ModelChoiceField(
        queryset=queryset,
        required=False,
    )
