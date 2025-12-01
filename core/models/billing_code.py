from django.core.exceptions import ValidationError
from django_generic_model_fields.create_generic_boolean import create_generic_boolean
from django_generic_model_fields.create_generic_fk import create_generic_fk
from django_generic_model_fields.create_generic_varchar import create_generic_varchar

from core.models.application import Application
from core.models.application_group import ApplicationGroup
from core.models.person import Person
from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName


class BillingCode(AbstractBaseModel, AbstractComment, AbstractName):
    application = create_generic_fk(to=Application)
    application_group = create_generic_fk(to=ApplicationGroup)
    billing_code = create_generic_varchar()
    is_active = create_generic_boolean(default=True)
    project_manager = create_generic_fk(to=Person, related_name='billing_codes_managed')
    replaces = create_generic_fk(to='self', related_name='replaced_by_codes')

    def clean(self):
        """Validate that the project manager has the Project Manager role."""
        super().clean()

        if self.project_manager:
            from core.models.role import Role

            try:
                project_manager_role = Role.objects.get(name='Project Manager')
            except Role.DoesNotExist:
                raise ValidationError({
                    'project_manager': 'The Project Manager role does not exist in the system.'
                })

            if not self.project_manager.roles.filter(id=project_manager_role.id).exists():
                raise ValidationError({
                    'project_manager': f'{self.project_manager} does not have the Project Manager role.'
                })

    def __str__(self):
        return f"{self.name} - {self.billing_code}"

    class Meta:
        ordering = ['-id']
