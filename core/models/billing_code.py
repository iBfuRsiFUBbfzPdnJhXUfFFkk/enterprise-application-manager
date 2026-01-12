from django.core.exceptions import ValidationError
from django.db import models

from core.models.application import Application
from core.models.application_group import ApplicationGroup
from core.models.person import Person
from core.models.team import Team
from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName


class BillingCode(AbstractBaseModel, AbstractComment, AbstractName):
    application = models.ForeignKey(Application, on_delete=models.SET_NULL, null=True, blank=True, related_name='billing_codes')
    application_group = models.ForeignKey(ApplicationGroup, on_delete=models.SET_NULL, null=True, blank=True, related_name='billing_codes')
    billing_code = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(null=True, blank=True, default=True)
    project_manager = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True, blank=True, related_name='billing_codes_managed')
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='billing_codes')
    replaces = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='replaced_by_codes')

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
