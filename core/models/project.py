from django.core.exceptions import ValidationError
from django.db import models

from core.models.application import Application
from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName
from core.models.person import Person

class Project(AbstractBaseModel, AbstractComment, AbstractName):
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('proposal_approved', 'Proposal Approved'),
        ('beta_launch', 'Beta Launch'),
        ('soft_launch', 'Soft Launch'),
        ('launched', 'Launched'),
        ('on_hold', 'On Hold'),
        ('denied', 'Denied'),
    ]

    applications = models.ManyToManyField(Application, blank=True, related_name="%(class)s_set")
    billing_codes = models.ManyToManyField('BillingCode', blank=True, related_name='projects')
    person_stake_holders = models.ManyToManyField(Person, blank=True, related_name="%(class)s_set")
    project_manager = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True, blank=True, related_name='projects_managed')
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, null=True, blank=True)

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
