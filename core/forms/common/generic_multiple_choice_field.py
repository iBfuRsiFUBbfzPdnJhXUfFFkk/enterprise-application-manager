from django.db.models import QuerySet
from django.forms import ModelMultipleChoiceField, CheckboxSelectMultiple


def generic_multiple_choice_field(
        queryset: QuerySet,
) -> ModelMultipleChoiceField:
    return ModelMultipleChoiceField(
        queryset=queryset,
        required=False,
        widget=CheckboxSelectMultiple
    )
