from typing import Any

from django.forms import ModelMultipleChoiceField

from core.forms.common.generic_multiple_choice_field import generic_multiple_choice_field
from core.models.person import Person
from core.models.role import Role


# Mapping of old boolean field names to role names for backward compatibility
ROLE_MAPPING = {
    'is_architect': 'Architect',
    'is_developer': 'Developer',
    'is_lead_developer': 'Lead Developer',
    'is_product_manager': 'Product Manager',
    'is_product_owner': 'Product Owner',
    'is_project_manager': 'Project Manager',
    'is_scrum_master': 'Scrum Master',
    'is_stakeholder': 'Stakeholder',
}


def generic_person_multiple_choice_field(
        **kwargs: Any
) -> ModelMultipleChoiceField:
    # Convert old boolean field filters to role-based filters
    # We need to defer the actual database query until the field is used
    role_filter_names = []
    other_filters = {}

    for key, value in kwargs.items():
        if key in ROLE_MAPPING and value is True:
            # This is a role filter, save the role name for later lookup
            role_filter_names.append(ROLE_MAPPING[key])
        else:
            # Regular filter (like is_employee, is_active, etc.)
            other_filters[key] = value

    # Build the queryset - this will be evaluated lazily
    queryset = Person.objects.all()

    # Apply role filters if any (using role names, not objects)
    if role_filter_names:
        # Filter by role names instead of role objects to avoid DB query at import time
        queryset = queryset.filter(roles__name__in=role_filter_names).distinct()

    # Apply other filters
    if other_filters:
        queryset = queryset.filter(**other_filters)

    return generic_multiple_choice_field(queryset=queryset)
