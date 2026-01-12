from django.db import models

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName
from core.models.common.enums.hr_incident_status_choices import HR_INCIDENT_STATUS_CHOICES


class HRIncident(AbstractBaseModel, AbstractName, AbstractComment):
    reference_number: str | None = models.CharField(max_length=255, null=True, blank=True)
    person = models.ForeignKey('core.Person', on_delete=models.SET_NULL, null=True, blank=True, related_name='hr_incidents')
    filed_by = models.ForeignKey('core.Person', on_delete=models.SET_NULL, null=True, blank=True, related_name='filed_hr_incidents')
    bad_interactions = models.ManyToManyField('core.BadInteraction', blank=True, related_name='hr_incidents')
    date_filed = models.DateField(null=True, blank=True)
    date_resolved: models.DateField | None = models.DateField(null=True, blank=True)
    description: str | None = models.TextField(blank=True, null=True, help_text='Detailed description')
    resolution: str | None = models.TextField(blank=True, null=True, help_text='Resolution details')
    status: str = models.CharField(max_length=255, choices=HR_INCIDENT_STATUS_CHOICES, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.name} - {self.person} ({self.status})"

    class Meta:
        ordering = ['-date_filed', 'id']
        verbose_name = "HR Incident"
        verbose_name_plural = "HR Incidents"
