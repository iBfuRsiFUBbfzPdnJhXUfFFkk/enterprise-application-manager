from django.core.exceptions import ValidationError
from django_generic_model_fields.create_generic_fk import create_generic_fk
from django_generic_model_fields.create_generic_m2m import create_generic_m2m
from django_generic_model_fields.create_generic_varchar import create_generic_varchar

from core.models.application import Application
from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName
from core.models.person import Person


class Project(AbstractBaseModel, AbstractComment, AbstractName):
    applications = create_generic_m2m(to=Application)
    billing_codes = create_generic_m2m(to='BillingCode', related_name='projects')
    person_stake_holders = create_generic_m2m(to=Person)
    project_manager = create_generic_fk(to=Person, related_name='projects_managed')

    def clean(self):
        """
        Validate that the project manager has the Project Manager role.
        """
        super().clean()

        if self.project_manager:
            from core.models.role import Role

            # Get the Project Manager role
            try:
                project_manager_role = Role.objects.get(name='Project Manager')
            except Role.DoesNotExist:
                raise ValidationError({
                    'project_manager': 'The Project Manager role does not exist in the system.'
                })

            # Check if the selected person has the Project Manager role
            if not self.project_manager.roles.filter(id=project_manager_role.id).exists():
                raise ValidationError({
                    'project_manager': f'{self.project_manager} does not have the Project Manager role.'
                })

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['name', '-id']
