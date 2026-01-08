from datetime import datetime

from django.db import models
from django.utils import timezone

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName
from core.models.common.enums.maintenance_severity_choices import MAINTENANCE_SEVERITY_CHOICES
from core.models.common.enums.maintenance_status_choices import MAINTENANCE_STATUS_CHOICES
from django_generic_model_fields.create_generic_datetime import create_generic_datetime
from django_generic_model_fields.create_generic_enum import create_generic_enum
from django_generic_model_fields.create_generic_fk import create_generic_fk
from django_generic_model_fields.create_generic_m2m import create_generic_m2m
from django_generic_model_fields.create_generic_text import create_generic_text


class MaintenanceWindow(AbstractBaseModel, AbstractComment, AbstractName):
    date_time_start = create_generic_datetime()
    date_time_end = create_generic_datetime()
    description = create_generic_text()
    severity = create_generic_enum(choices=MAINTENANCE_SEVERITY_CHOICES)
    status = create_generic_enum(choices=MAINTENANCE_STATUS_CHOICES)
    applications_affected = create_generic_m2m(to='Application', related_name='maintenance_windows')
    person_contact = create_generic_fk(to='Person', related_name='maintenance_windows_as_contact')
    person_created_by = create_generic_fk(to='Person', related_name='maintenance_windows_created')

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
