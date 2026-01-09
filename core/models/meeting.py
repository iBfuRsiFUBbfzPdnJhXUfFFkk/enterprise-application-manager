from datetime import datetime

from django.db import models
from django.utils import timezone

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_location import AbstractLocation
from core.models.common.abstract.abstract_name import AbstractName
from core.models.common.enums.meeting_status_choices import MEETING_STATUS_CHOICES
from core.models.common.enums.meeting_type_choices import MEETING_TYPE_CHOICES
from django_generic_model_fields.create_generic_datetime import create_generic_datetime
from django_generic_model_fields.create_generic_enum import create_generic_enum
from django_generic_model_fields.create_generic_fk import create_generic_fk
from django_generic_model_fields.create_generic_m2m import create_generic_m2m
from django_generic_model_fields.create_generic_text import create_generic_text
from django_generic_model_fields.create_generic_varchar import create_generic_varchar


class Meeting(AbstractBaseModel, AbstractComment, AbstractName, AbstractLocation):
    datetime_start = create_generic_datetime()
    datetime_end = create_generic_datetime()
    description = create_generic_text()
    agenda = create_generic_text()
    minutes = create_generic_text()
    organizer = create_generic_fk(to='Person', related_name='meetings_organized')
    attendees = create_generic_m2m(to='Person', related_name='meetings_attended')
    actual_attendees = create_generic_m2m(to='Person', related_name='meetings_actually_attended')
    application = create_generic_fk(to='Application', related_name='meetings')
    project = create_generic_fk(to='Project', related_name='meetings')
    meeting_type = create_generic_enum(choices=MEETING_TYPE_CHOICES)
    status = create_generic_enum(choices=MEETING_STATUS_CHOICES)
    virtual_meeting_url = create_generic_varchar()

    @property
    def duration_hours(self) -> float:
        if self.datetime_start and self.datetime_end:
            delta = self.datetime_end - self.datetime_start
            return round(delta.total_seconds() / 3600, 2)
        return 0.0

    @property
    def is_in_progress(self) -> bool:
        now = timezone.now()
        if self.datetime_start and self.datetime_end:
            return self.datetime_start <= now <= self.datetime_end
        return False

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        ordering = ['-datetime_start', '-id']
        indexes = [
            models.Index(fields=['datetime_start']),
            models.Index(fields=['datetime_end']),
            models.Index(fields=['status']),
            models.Index(fields=['meeting_type']),
        ]
