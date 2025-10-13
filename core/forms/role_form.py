from django.forms import ModelMultipleChoiceField, SelectMultiple

from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.person import Person
from core.models.role import Role


class RoleForm(BaseModelForm):
    # Use SelectMultiple widget for people field (for searchable chip selector component)
    people = ModelMultipleChoiceField(
        queryset=Person.objects.all().order_by('name_last', 'name_first'),
        required=False,
        widget=SelectMultiple(attrs={'class': 'searchable-multi-select'}),
        label='People with this Role'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Populate reverse M2M relationship for editing
        if self.instance and self.instance.pk:
            # Load existing people who have this role
            self.fields['people'].initial = self.instance.people_who_hold_this_role.all()

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()

        # Save reverse M2M relationship - update people's roles
        if self.instance.pk and 'people' in self.cleaned_data:
            # Get the current people who should have this role
            selected_people = self.cleaned_data['people']

            # Get the current people who have this role
            current_people = set(self.instance.people_who_hold_this_role.all())
            selected_people_set = set(selected_people)

            # Remove this role from people who no longer should have it
            people_to_remove = current_people - selected_people_set
            for person in people_to_remove:
                person.roles.remove(self.instance)

            # Add this role to people who should have it
            people_to_add = selected_people_set - current_people
            for person in people_to_add:
                person.roles.add(self.instance)

        return instance

    class Meta(BaseModelFormMeta):
        model = Role
