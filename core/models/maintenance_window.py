from datetime import datetime

from django.db import models
from django.utils import timezone

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName
from core.models.common.enums.maintenance_severity_choices import MAINTENANCE_SEVERITY_CHOICES
from core.models.common.enums.maintenance_status_choices import MAINTENANCE_STATUS_CHOICES

class MaintenanceWindow(AbstractBaseModel, AbstractComment, AbstractName):
    date_time_start = models.DateTimeField(null=True, blank=True)
    date_time_end = models.DateTimeField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    severity = models.CharField(max_length=255, choices=MAINTENANCE_SEVERITY_CHOICES, null=True, blank=True)
    status = models.CharField(max_length=255, choices=MAINTENANCE_STATUS_CHOICES, null=True, blank=True)
    applications_affected = models.ManyToManyField('Application', blank=True, related_name='maintenance_windows')
    person_contact = models.ForeignKey('Person', on_delete=models.SET_NULL, null=True, blank=True, related_name='maintenance_windows_as_contact')
    person_created_by = models.ForeignKey('Person', on_delete=models.SET_NULL, null=True, blank=True, related_name='maintenance_windows_created')

    @property
    def duration_hours(self) -> float:
        if self.date_time_start and self.date_time_end:
            delta = self.date_time_end - self.date_time_start
            return round(delta.total_seconds() / 3600, 2)
        return 0.0

    @property
    def is_in_progress(self) -> bool:
        now = timezone.now()
        if self.date_time_start and self.date_time_end:
            return self.date_time_start <= now <= self.date_time_end
        return False

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        ordering = ['-date_time_start', '-id']
        indexes = [
            models.Index(fields=['date_time_start']),
            models.Index(fields=['date_time_end']),
            models.Index(fields=['status']),
        ]
