from django.db import models
from django_generic_model_fields.create_generic_date import create_generic_date
from django_generic_model_fields.create_generic_enum import create_generic_enum
from django_generic_model_fields.create_generic_fk import create_generic_fk
from django_generic_model_fields.create_generic_m2m import create_generic_m2m
from django_generic_model_fields.create_generic_varchar import create_generic_varchar

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName
from core.models.common.enums.hr_incident_status_choices import HR_INCIDENT_STATUS_CHOICES


class HRIncident(AbstractBaseModel, AbstractName, AbstractComment):
    reference_number: str | None = create_generic_varchar()
    person = create_generic_fk(to='core.Person', related_name='hr_incidents')
    filed_by = create_generic_fk(to='core.Person', related_name='filed_hr_incidents')
    bad_interactions = create_generic_m2m(to='core.BadInteraction', related_name='hr_incidents')
    date_filed = create_generic_date()
    date_resolved: models.DateField | None = create_generic_date()
    description: str | None = models.TextField(blank=True, null=True, help_text='Detailed description')
    resolution: str | None = models.TextField(blank=True, null=True, help_text='Resolution details')
    status: str = create_generic_enum(choices=HR_INCIDENT_STATUS_CHOICES)

    def __str__(self) -> str:
        return f"{self.name} - {self.person} ({self.status})"

    class Meta:
        ordering = ['-date_filed', 'id']
        verbose_name = "HR Incident"
        verbose_name_plural = "HR Incidents"
